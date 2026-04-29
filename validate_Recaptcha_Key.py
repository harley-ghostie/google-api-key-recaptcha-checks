import requests

def test_recaptcha_sitekey_restriction(site_key, test_domain):
    """
    Test if a reCAPTCHA site key is restricted to specific domains.

    Args:
        site_key (str): The reCAPTCHA site key to test.
        test_domain (str): The domain to simulate for testing the restriction.

    Returns:
        bool: True if the site key works on the test domain, False otherwise.
    """
    # URL for the reCAPTCHA anchor endpoint
    recaptcha_url = "https://www.google.com/recaptcha/api2/anchor"

    # Parameters for the GET request
    params = {
        "ar": 1,
        "k": site_key,
        "co": "exemplo.com.br",
        "hl": "en",
        "v": "RTbEo8_aWOvLbjGuoA8Hj2oS",
        "size": "invisible",
        "cb": "test"
    }

    try:
        response = requests.get(recaptcha_url, params=params, headers={"Referer": test_domain})

        if response.status_code == 200:
            # Check if the response contains an error related to domain restriction
            if "error" in response.text.lower():
                print(f"The site key does not work on the test domain {test_domain}. It may be restricted.")
                return False
            else:
                print(f"The site key works on the test domain {test_domain}. It may not be restricted.")
                return True
        else:
            print(f"Failed to connect to the reCAPTCHA service. Status code: {response.status_code}")
            return False

    except requests.RequestException as e:
        print(f"An error occurred while connecting to the reCAPTCHA service: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Replace with the site key you want to test
   test_site_key = "SITE_KEY_RECAPTCHA_AQUI"

    # Replace with a test domain (you should control this domain for ethical testing)
   test_domain = "https://dominio-teste.com.br"

    # Test the site key
    is_restricted = test_recaptcha_sitekey_restriction(test_site_key, test_domain)

    if is_restricted:
        print("The site key is not properly restricted to specific domains.")
    else:
        print("The site key appears to be properly restricted to specific domains.")
