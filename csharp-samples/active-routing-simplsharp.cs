using System;
using System.Net.Http;
// using System.Net.Http;
using Crestron.SimplSharp.Net.Https;
using Newtonsoft.Json;

namespace activerouting_461
{
    class Program
    {
        static readonly string PODIP = "https://10.0.0.196:5443";
        static readonly string SINKIP = "10.0.0.186";

        public class AccessToken
        {
            public string access_token { get; set; }

        }


        public class ConfigRequest
        {
            // "{\"presence\": false, \"message\": \"Im Sharing!\", \"background\": \"#B8BDBF\", \"foreground\": \"#FFFFFF\", \"audio\": false}"
            public bool presence { get; set; }
            public string message { get; set; }
            public string background { get; set; }
            public string foreground { get; set; }
            // public bool audio { get; set; }

        }

        public class SinkRequest
        {
            // "{\"post\": \"fullscreen\", \"message\": \"Testing from API\", \"foreground\": \"#FFFFFF\", \"background\": \"#B8BDBF\", \"resolution\": \"1920x1080\", \"sink\": \"192.168.128.196\"}"
            public string post { get; set; }
            public string message { get; set; }
            public string background { get; set; }
            public string foreground { get; set; }
            public string resolution { get; set; }
            public string sink { get; set; }

        }

        static void Main(string[] args)
        {

            // HttpClient is intended to be instantiated once per application, rather than per-use. See Remarks.
            HttpsClient client = new HttpsClient();
            AccessToken token;
            HttpsHeader authHeader;

            client.PeerVerification = false;
            client.HostVerification = false;

            try
            {

                // Create and send the auth request

                HttpsClientRequest aRequest = new HttpsClientRequest();
                string aUrl = PODIP + "/v2/token";
                aRequest.Url.Parse(aUrl);
                aRequest.RequestType = RequestType.Post;
                aRequest.Header.ContentType = "application/x-www-form-urlencoded";
                aRequest.ContentString = "grant_type=password&username=admin&password=";

                HttpsClientResponse authResponse = client.Dispatch(aRequest);

                token = JsonConvert.DeserializeObject<AccessToken>(authResponse.ContentString);
                authHeader = new HttpsHeader("Authorization", "Bearer " + token.access_token);
                Console.WriteLine(token.access_token);

                // ------------------------------------------------------------
                // Create and send the Patch or Post
                // ------------------------------------------------------------

                // String requestBody = "{\"presence\": false, \"message\": \"I'm Sharing!\", \"background\": \"#B8BDBF\", \"foreground\": \"#FFFFFF\"}";
                // String requestBody = "{\"presence\": false, \"message\": \"Im Sharing!\", \"background\": \"#B8BDBF\", \"foreground\": \"#FFFFFF\", \"audio\": false}";

                ConfigRequest requestBody = new ConfigRequest()
                {

                    presence = false,
                    message = "Im Sharing",
                    background = "#B8BDBF",
                    foreground = "#FFFFFF"
                };

                String responseBody = String.Empty;
                var jsonRequest = JsonConvert.SerializeObject(requestBody);

                HttpsClientRequest configRequest = new HttpsClientRequest();
                string confUrl = PODIP + "/v2/content/activerouting";
                configRequest.Url.Parse(confUrl);
                // BUG: There is a known issue with the SimplSharp PATCH
                // method. This method will not succeed using the SimplSharp.
                // This step is optional in setting up an Active Routing session,
                // and can be skipped if using SimplSharp.
                configRequest.RequestType = RequestType.Patch;
                configRequest.Header.ContentType = "application/json";
                configRequest.ContentString = jsonRequest;
                configRequest.Header.AddHeader(authHeader);

                HttpsClientResponse configResponse = client.Dispatch(configRequest);

                Console.WriteLine(configResponse.ContentString);

                //    // ------------------------------------------------------------
                //    // Create and send the sink 
                //    // ------------------------------------------------------------

                //    // String requestBody = "{\"presence\": false, \"message\": \"I'm Sharing!\", \"background\": \"#B8BDBF\", \"foreground\": \"#FFFFFF\"}";
                //    // String sinkBody = "{\"post\": \"fullscreen\", \"message\": \"Testing from API\", \"foreground\": \"#FFFFFF\", \"background\": \"#B8BDBF\", \"resolution\": \"1920x1080\", \"sink\": \"192.168.128.196\"}";

                SinkRequest sinkBody = new SinkRequest()
                {
                    post = "fullscreen",
                    message = "Testing from API",
                    foreground = "#FFFFFF",
                    background = "#B8BDBF",
                    resolution = "1920x1080",
                    sink = SINKIP
                };

                String responseBody_Sink = String.Empty;
                var jsonRequest_Sink = JsonConvert.SerializeObject(sinkBody);

                HttpsClientRequest sinkRequest = new HttpsClientRequest();
                string sinkUrl = PODIP + "/v2/content/activerouting/connections";
                sinkRequest.Url.Parse(sinkUrl);
                sinkRequest.RequestType = RequestType.Post;
                sinkRequest.Header.ContentType = "application/json";
                sinkRequest.ContentString = jsonRequest;
                sinkRequest.Header.AddHeader(authHeader);

                HttpsClientResponse sinkResponse = client.Dispatch(sinkRequest);

                Console.WriteLine(sinkResponse.ContentString);

            }
            catch (HttpRequestException e)
            {
                Console.WriteLine("\nException Caught!");
                Console.WriteLine("Message :{0} ", e.Message);
            }


        }
    }
}
