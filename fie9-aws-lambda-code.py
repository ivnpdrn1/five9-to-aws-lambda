import os
import requests
from requests.auth import HTTPBasicAuth

def lambda_handler(event, context):
    # Five9 API credentials
    username = os.environ['FIVE9_USERNAME-ask Mark']
    password = os.environ['FIVE9_PASSWORD-ask Mark']
    
    # Five9 API URL
    api_url = "https://api.five9.com/wsadmin/v4/AdminWebService"

    # SOAP request to run a report
    soap_request = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.admin.ws.five9.com/">
        <soapenv:Header/>
        <soapenv:Body>
            <ser:runReport>
                <folderName>1Call Control (IP) (Sunshine Life)</folderName>
                <reportName>Vlookup Report export 1</reportName>
                <criteria>
                    <time>
                        <end>2020-05-10T23:00:00.000-07:00</end>
                        <start>2020-05-01T00:00:00.000-07:00</start>
                    </time>
                </criteria>
            </ser:runReport>
        </soapenv:Body>
    </soapenv:Envelope>
    """

    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    # Send the SOAP request to the Five9 API
    try:
        response = requests.post(api_url, data=soap_request, headers=headers, auth=HTTPBasicAuth(username, password))
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the SOAP response
            unique_identifier = parse_run_report_response(response.text)
            return {
                "statusCode": 200,
                "body": f"Report requested successfully. Unique Identifier: {unique_identifier}"
            }
        else:
            return {
                "statusCode": response.status_code,
                "body": f"Error: {response.text}"
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }

def parse_run_report_response(response_text):
    # Parse the XML response to extract the unique identifier
    import xml.etree.ElementTree as ET
    root = ET.fromstring(response_text)
    namespace = {'ns2': 'http://service.admin.ws.five9.com/'}
    unique_identifier = root.find('.//ns2:return', namespace).text
    return unique_identifier
