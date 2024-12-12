# from .tracking.platform import HubPlatform, TensorflowPlatform, PytorchLightningPlatform, MLFlowPlatform, KerasPlatform
import os
import time
import inspect

# from turihub import Hub
# import neptune.new as neptune
# from tensorboardX import SummaryWriter
# import pytorch_lightning as pl
# import mlflow
import requests
from datetime import datetime, timezone


class PlatformType:
    HUB = "turihub"
    # NEPTUNE = "neptune"
    TENSORFLOW = "tensorflow"
    PYTORCH_LIGHTNING = "pytorch_lightning"
    PYTORCH = "pytorch"
    MLFLOW = "mlflow"
    KERAS = "keras"


def init_experiment(experiment_name, platform_type, owner_email=None, **kwargs):
    caller_frame = inspect.stack()[1]
    source_file_path = caller_frame.filename
    source_file_name = os.path.basename(source_file_path)  # Extract just the file name

    if platform_type == PlatformType.HUB:
        return HubPlatform(**kwargs)
    elif platform_type == PlatformType.TENSORFLOW:
        return TensorflowPlatform(**kwargs)
    elif platform_type == PlatformType.PYTORCH_LIGHTNING:
        return PytorchLightningPlatform(experiment_name=experiment_name, owner_email=owner_email, **kwargs)
    elif platform_type == PlatformType.PYTORCH:
        return PytorchPlatform(experiment_name=experiment_name, owner_email=owner_email, source_file_path=source_file_path, source_file_name=source_file_name, **kwargs)
    elif platform_type == PlatformType.MLFLOW:
        return MLFlowPlatform(**kwargs)
    elif platform_type == PlatformType.KERAS:
        return KerasPlatform(experiment_name=experiment_name, owner_email=owner_email, **kwargs)
    else:
        raise ValueError(f"Unsupported platform type: {platform_type}")


class BasePlatform:
    """
    Base platform class to define common methods across platforms.
    """

    def __init__(self, experiment_name="default", owner_email=None, **kwargs):
        self.experiment_name = experiment_name
        self.owner_email = owner_email

    def setOwnerEmail(self, owner_email):
        self.owner_email = owner_email

    def log_metric(self, name, value, step=None):
        raise NotImplementedError("log_metric must be implemented in subclasses.")

    def log_image(self, name, image, step=None):
        raise NotImplementedError("log_image must be implemented in subclasses.")

    def stop(self):
        raise NotImplementedError("stop must be implemented in subclasses.")

    def send_source_file(self, source_file_path, source_file_name, flask_url, experiment_id, run_id, artifact_type):
        try:
            # Construct the URL with query parameters
            url_with_params = f"{flask_url}?experiment_id={experiment_id}&run_id={run_id}&artifact_type={artifact_type}"

            # Send the source file to the Flask backend
            with open(source_file_path, 'rb') as f:
                files = {'file': (source_file_name, f)}

                # Debug: Log request details
                print(f"Sending POST request to {url_with_params}")
                print(f"Files: {files}")

                response = requests.post(url_with_params, files=files)

                # Debug: Print response status and content
                print(f"Response Status Code: {response.status_code}")
                print(f"Response Content: {response.content.decode('utf-8', errors='ignore')}")

                if response.headers.get('Content-Type') == 'application/json':
                    return response.json()
                else:
                    raise ValueError(f"Unexpected response format: {response.content.decode('utf-8', errors='ignore')}")
        except requests.RequestException as e:
            print(f"Failed to send source file: {e}")
            raise e

    def upload_the_source(self, flask_url, source_file_path, source_file_name):

        try:

            # Upload the file to the Flask backend
            result = self.send_source_file(source_file_path, source_file_name, flask_url, self.experiment_id, self.run_id, "source_file")

            return result

        except requests.RequestException as e:
            print(f"Failed to upload source file: {e}")
            raise e

class AppendableMetric:
    def __init__(self, platform, key):
        self.platform = platform  # Reference to the PytorchPlatform instance
        self.key = key
        self.values = []  # Local cache for values (optional)

    def append(self, value):
        """
        Append a value to the metric and log it immediately to the server.
        """
        self.values.append(value)
        self.platform.log_metric(self.key, value, step=len(self.values))  # Use length of values as step


class PytorchPlatform(BasePlatform):
    """
    Platform class for logging data via PyTorch logger.
    """

    def __init__(self, experiment_name="default", owner_email=None, source_file_path=None, source_file_name=None, **kwargs):
        # Initialize the BasePlatform with any required arguments
        super().__init__(experiment_name, owner_email, **kwargs)
        self.experiment_running = True
        self.total_epochs = 0
        self.current_epoch = 0
        self.appendable_metrics = {}  # Store appendable metrics
        # self.logger = logger or pl.loggers.TensorBoardLogger("logs/")
        try:

            # Load environment variables
            IN_DEV_MODE = os.getenv("IN_DEV_MODE", "false").lower() == "true"
            # USE_BETA_URL = os.getenv("USE_BETA_URL", "false").lower() == "true"
            USE_BETA_URL = True # force to true for now for testing in beta

            if (IN_DEV_MODE):
                config_url = "http://localhost:8080/api/login/getConfigModeAndVersionREST"
                print(f"Using dev mode, fetching config from {config_url}")
                response = requests.get(config_url)
            else:
                if (USE_BETA_URL):
                    config_url = "https://beta-mlops.infoapps.apple.com/api/login/getConfigModeAndVersionREST"
                    print(f"Using beta mode, fetching config from {config_url}")
                    response = requests.get(config_url)
                else:
                    config_url = "https://mlops.infoapps.apple.com/api/login/getConfigModeAndVersionREST"
                    print(f"Using prod mode, fetching config from {config_url}")
                    response = requests.get(config_url)

            response.raise_for_status()  # Raises an error for bad status codes
            config_data = response.json()

            # Use prodUrl or devUrl based on environment mode
            if config_data["environment_mode"] == "production":
                self.server_url = config_data["prodUrl"]
                if (config_data['environment_mode'] != "kube"):
                    self.server_url = "http://localhost:8080"
            else:
                self.server_url = config_data["devUrl"]
                if (config_data['environment_mode'] != "kube"):
                    self.server_url = "http://localhost:8080"
            print(f"server_url: {self.server_url}")

        except requests.RequestException as e:
            print(f"Error retrieving server URL from config: {e}")
            self.server_url = "https://mlops.infoapps.apple.com"  # Set a fallback if the request fails

        print(f"Server URL set to: {self.server_url}")

        self.run_id = None  # Store the run ID for updating later

        # Create or check the experiment on initialization
        response = requests.post(
            f"{self.server_url}/api/experiments/check_or_create",
            json={
                "experiment_name": experiment_name,
                "platform_type": "pytorch",
                "owner_email": owner_email
            }
        )

        if response.status_code == 200:
            data = response.json()
            self.experiment_id = data.get("experiment_id")  # Store the experiment ID
            self.run_id = data.get("run_id")  # Store the run ID if it's returned from the server

            source_url = f"{self.server_url}/api/experiments/uploadArtifact"
            self.upload_the_source(source_url, source_file_path, source_file_name)

            print(f"Source file: {source_file_name} uploaded to: {source_url}")
        else:
            raise Exception("Failed to create or retrieve experiment.")

    def __setitem__(self, key, value):
        """
        Handles `experiment["key"] = value`.
        """
        if isinstance(value, AppendableMetric):
            self.appendable_metrics[key] = value
        else:
            self.log_metric(key, value)

    def __getitem__(self, key):
        """
        Return an AppendableMetric object for a key to allow appending.
        """
        if key not in self.appendable_metrics:
            self.appendable_metrics[key] = AppendableMetric(self, key)
        return self.appendable_metrics[key]

    def log_metric(self, name, value, step=None):
        """
        Logs a single metric to the server.
        """
        print(f"Logging metric: {name} = {value} (Step: {step})")
        payload = {
            "experiment_id": self.experiment_id,
            "run_id": self.run_id,
            "metric_name": name,
            "metric_value": value,
            "step": step,
            "is_multi_value": True if name in self.appendable_metrics else False,
        }
        try:
            response = requests.post(f"{self.server_url}/api/experiments/log_metric", json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to log metric {name}: {e}")

    def log_image(self, name, image, step=None):
        # PyTorch Lightning does not directly support image logging in the default loggers.
        pass

    def done(self):
        """
                Stop the experiment run and mark it as finished.
                """
        if not self.run_id:
            raise Exception("Run ID not set. Unable to stop the run.")

        # while self.experiment_running:
        #     print("Waiting for experiment to finish running...")
        #     time.sleep(5)

        all_logged = False
        while not all_logged:
            response = requests.get(f"{self.server_url}/api/experiments/check_metrics_logged",
                                    params={"experiment_id": self.experiment_id
                                        , "run_id": self.run_id})
            data = response.json()
            epochs_logged = data["epochs_logged"]

            if epochs_logged != self.total_epochs:
                # print(f"Waiting for {data['not_logged_count']} metrics to be logged...")
                time.sleep(5)  # Poll every 2 seconds
            else:
                all_logged = True

        response = requests.post(
            f"{self.server_url}/api/experiments/stop_run",
            json={
                "run_id": self.run_id,
                "state": "COMPLETED"
            }
        )

        if response.status_code == 200:
            print(f"Run {self.run_id} marked as COMPLETED.")
        else:
            raise Exception("Failed to stop the run.")


class PytorchLightningPlatform(BasePlatform):
    """
    Platform class for logging data via PyTorch Lightning's built-in logger.
    """

    def __init__(self, experiment_name="default", owner_email=None, **kwargs):
        # Initialize the BasePlatform with any required arguments
        super().__init__(experiment_name, owner_email, **kwargs)
        self.experiment_running = True
        self.total_epochs = 0
        self.current_epoch = 0
        # self.logger = logger or pl.loggers.TensorBoardLogger("logs/")
        try:

            # Load environment variables
            IN_DEV_MODE = os.getenv("IN_DEV_MODE", "false").lower() == "true"
            # USE_BETA_URL = os.getenv("USE_BETA_URL", "false").lower() == "true"
            USE_BETA_URL = True # force to true for now for testing in beta

            if (IN_DEV_MODE):
                config_url = "http://localhost:8080/api/login/getConfigModeAndVersionREST"
                print(f"Using dev mode, fetching config from {config_url}")
                response = requests.get(config_url)
            else:
                if (USE_BETA_URL):
                    config_url = "https://beta-mlops.infoapps.apple.com/api/login/getConfigModeAndVersionREST"
                    print(f"Using beta mode, fetching config from {config_url}")
                    response = requests.get(config_url)
                else:
                    config_url = "https://mlops.infoapps.apple.com/api/login/getConfigModeAndVersionREST"
                    print(f"Using prod mode, fetching config from {config_url}")
                    response = requests.get(config_url)

            response.raise_for_status()  # Raises an error for bad status codes
            config_data = response.json()

            # Use prodUrl or devUrl based on environment mode
            if config_data["environment_mode"] == "production":
                self.server_url = config_data["prodUrl"]
                if (config_data['environment_mode'] != "kube"):
                    self.server_url = "http://localhost:8080"
            else:
                self.server_url = config_data["devUrl"]
                if (config_data['environment_mode'] != "kube"):
                    self.server_url = "http://localhost:8080"
            print(f"server_url: {self.server_url}")

        except requests.RequestException as e:
            print(f"Error retrieving server URL from config: {e}")
            self.server_url = "https://mlops.infoapps.apple.com"  # Set a fallback if the request fails

        print(f"Server URL set to: {self.server_url}")

        self.run_id = None  # Store the run ID for updating later

        # Create or check the experiment on initialization
        response = requests.post(
            f"{self.server_url}/api/experiments/check_or_create",
            json={
                "experiment_name": experiment_name,
                "platform_type": "pytorch-lightning",
                "owner_email": owner_email
            }
        )

        if response.status_code == 200:
            data = response.json()
            self.experiment_id = data.get("experiment_id")  # Store the experiment ID
            self.run_id = data.get("run_id")  # Store the run ID if it's returned from the server
        else:
            raise Exception("Failed to create or retrieve experiment.")

    def log_metric(self, name, value, step=None):
        print(f"Logging metric {name} with value {value}")
        # if step:
        #     # self.logger.log_metrics({name: value}, step)
        #     ...
        # else:
        #     # self.logger.log_metrics({name: value})
        #     ...

    def log_image(self, name, image, step=None):
        # PyTorch Lightning does not directly support image logging in the default loggers.
        pass

    def done(self):
        """
                Stop the experiment run and mark it as finished.
                """
        if not self.run_id:
            raise Exception("Run ID not set. Unable to stop the run.")

        # while self.experiment_running:
        #     print("Waiting for experiment to finish running...")
        #     time.sleep(5)

        all_logged = False
        while not all_logged:
            response = requests.get(f"{self.server_url}/api/experiments/check_metrics_logged",
                                    params={"experiment_id": self.experiment_id
                                        , "run_id": self.run_id})
            data = response.json()
            epochs_logged = data["epochs_logged"]

            if epochs_logged != self.total_epochs:
                # print(f"Waiting for {data['not_logged_count']} metrics to be logged...")
                time.sleep(5)  # Poll every 2 seconds
            else:
                all_logged = True

        response = requests.post(
            f"{self.server_url}/api/experiments/stop_run",
            json={
                "run_id": self.run_id,
                "state": "COMPLETED"
            }
        )

        if response.status_code == 200:
            print(f"Run {self.run_id} marked as COMPLETED.")
        else:
            raise Exception("Failed to stop the run.")



class KerasPlatform(BasePlatform):
    """
    Platform class for logging data specific to Keras.
    """

    def __init__(self, experiment_name="default", owner_email=None, **kwargs):
        # Initialize the BasePlatform with any required arguments
        super().__init__(experiment_name, owner_email, **kwargs)
        self.experiment_running = True
        self.total_epochs = 0
        self.current_epoch = 0

        # If server_url is not provided, fetch it from the config endpoint

        try:

            # Load environment variables
            IN_DEV_MODE = os.getenv("IN_DEV_MODE", "false").lower() == "true"
            # USE_BETA_URL = os.getenv("USE_BETA_URL", "false").lower() == "true"
            USE_BETA_URL = True # force to true for now for testing in beta

            if (IN_DEV_MODE):
                config_url = "http://localhost:8080/api/login/getConfigModeAndVersionREST"
                print(f"Using dev mode, fetching config from {config_url}")
                response = requests.get(config_url)
            else:
                if (USE_BETA_URL):
                    config_url = "https://beta-mlops.infoapps.apple.com/api/login/getConfigModeAndVersionREST"
                    print(f"Using beta mode, fetching config from {config_url}")
                    response = requests.get(config_url)
                else:
                    config_url = "https://mlops.infoapps.apple.com/api/login/getConfigModeAndVersionREST"
                    print(f"Using prod mode, fetching config from {config_url}")
                    response = requests.get(config_url)

            response.raise_for_status()  # Raises an error for bad status codes
            config_data = response.json()

            # Use prodUrl or devUrl based on environment mode
            if config_data["environment_mode"] == "production":
                self.server_url = config_data["prodUrl"]
                if (config_data['environment_mode'] != "kube"):
                    self.server_url = "http://localhost:8080"
            else:
                self.server_url = config_data["devUrl"]
                if (config_data['environment_mode'] != "kube"):
                    self.server_url = "http://localhost:8080"
            print(f"server_url: {self.server_url}")

        except requests.RequestException as e:
            print(f"Error retrieving server URL from config: {e}")
            self.server_url = "https://mlops.infoapps.apple.com"  # Set a fallback if the request fails

        print(f"Server URL set to: {self.server_url}")

        self.run_id = None  # Store the run ID for updating later

        # Create or check the experiment on initialization
        response = requests.post(
            f"{self.server_url}/api/experiments/check_or_create",
            json={
                "experiment_name": experiment_name,
                "platform_type": "keras",
                "owner_email": owner_email
            }
        )

        if response.status_code == 200:
            data = response.json()
            self.experiment_id = data.get("experiment_id")  # Store the experiment ID
            self.run_id = data.get("run_id")  # Store the run ID if it's returned from the server
        else:
            raise Exception("Failed to create or retrieve experiment.")

    def log_metric(self, name, value, step=None):
        print(f"Logging metric {name} with value {value}")

    def log_image(self, name, image, step=None):
        # Implementation for logging images in KerasPlatform
        pass

    def log_param(self, name, value):
        # Implementation for logging parameters in KerasPlatform
        pass

    def experiment_done_running(self):
        self.experiment_running = False

    def done(self):
        """
        Stop the experiment run and mark it as finished.
        """
        if not self.run_id:
            raise Exception("Run ID not set. Unable to stop the run.")


        # while self.experiment_running:
        #     print("Waiting for experiment to finish running...")
        #     time.sleep(5)

        all_logged = False
        while not all_logged:
            response = requests.get(f"{self.server_url}/api/experiments/check_metrics_logged",
                                    params={"experiment_id": self.experiment_id
                                            , "run_id": self.run_id})
            data = response.json()
            epochs_logged = data["epochs_logged"]

            if epochs_logged != self.total_epochs:
                # print(f"Waiting for {data['not_logged_count']} metrics to be logged...")
                time.sleep(5)  # Poll every 2 seconds
            else:
                all_logged = True

        response = requests.post(
            f"{self.server_url}/api/experiments/stop_run",
            json={
                "run_id": self.run_id,
                "state": "COMPLETED"
            }
        )

        if response.status_code == 200:
            print(f"Run {self.run_id} marked as COMPLETED.")
        else:
            raise Exception("Failed to stop the run.")


class HubPlatform(BasePlatform):
    """
    Platform class for logging data to Hub platform.
    """

    def __init__(self, api_token, **kwargs):
        # self.platform = Hub(apikey=api_token, **kwargs)
        self.platform = None
        ...
    def getHubInstance(self):
        return self.platform

    def __getattr__(self, name):
        """
        Automatically forward any unrecognized attribute/method calls to the Hub instance.
        """
        return getattr(self.platform, name)

    def list_experiments(self, projectname):
        project = self.platform.project(projectname)
        experiments = project.experiments.experiments()
        return experiments

    def log_metric(self, name, value, step=None):
        self.platform[name].log(value, step=step)

    def log_image(self, name, image, step=None):
        self.platform[name].upload(image)

    def stop(self):
        self.platform.stop()


# class NeptunePlatform(BasePlatform):
#     """
#     Platform class for logging data to Neptune.
#     """
#     def __init__(self, project, api_token, **kwargs):
#         self.run = neptune.init_run(project=project, api_token=api_token, **kwargs)
#
#     def log_metric(self, name, value, step=None):
#         self.run[name].log(value, step=step)
#
#     def log_image(self, name, image, step=None):
#         self.run[name].upload(image)
#
#     def stop(self):
#         self.run.stop()


class TensorflowPlatform(BasePlatform):
    """
    Platform class for logging data to TensorBoard.
    """

    def __init__(self, log_dir="logs"):
        # self.writer = SummaryWriter(log_dir)
        ...

    def log_metric(self, name, value, step=None):
        self.writer.add_scalar(name, value, global_step=step)

    def log_image(self, name, image, step=None):
        self.writer.add_image(name, image, global_step=step)

    def stop(self):
        self.writer.close()









class MLFlowPlatform(BasePlatform):
    """
    Platform class for logging data to MLFlow.
    """

    def __init__(self, experiment_name="default"):
        # mlflow.set_experiment(experiment_name)
        # self.run = mlflow.start_run()
        ...

    def log_metric(self, name, value, step=None):
        # mlflow.log_metric(name, value, step=step)
        ...
    def log_image(self, name, image, step=None):
        # MLFlow logs images as artifacts
        # mlflow.log_artifact(image, artifact_path=name)
        ...
    def log_param(self, name, value):
        # mlflow.log_param(name, value)
        ...
    def stop(self):
        # mlflow.end_run()
        ...
