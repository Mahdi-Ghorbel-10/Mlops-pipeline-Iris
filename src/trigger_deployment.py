import requests

#  Define the Django API URL
DEPLOYMENT_URL = "http://127.0.0.1:8000/api/deploy/"

def trigger_deployment():
    """ Calls the Django API to reload the latest MLflow model """
    try:
        response = requests.post(DEPLOYMENT_URL)

        if response.status_code == 200:
            print(" Model successfully deployed via Django API!")
        else:
            print(f"Deployment failed: {response.text}")
    except Exception as e:
        print(f" Error in triggering deployment: {str(e)}")

# ✅ Run the function if executed as a script
if __name__ == "__main__":
    trigger_deployment()
