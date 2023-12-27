using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

class Program
{
    static readonly HttpClient client = new HttpClient();

    static async Task Main(string[] args)
    {
        string email = "fake@email.com";
        string password = "password";

        var tokens = await AuthenticateUser(email, password);
        Console.WriteLine($"{tokens}");

        if (tokens != null)
        {
            //await CreateDevice(tokens.access_token);
            await CreateDeviceReq(tokens);
        }
    }

    static async Task<String> AuthenticateUser(string email, string password)
    {
        //var url = "https://gargantuan-unwritten-carp.gigalixirapp.com/api/v1/session";
        var url = "http://localhost:4000/api/v1/session";
        var userData = new
        {
            user = new { email, password }
        };
        var data = JsonConvert.SerializeObject(userData);
        var content = new StringContent(data, Encoding.UTF8, "application/json");
        var response = await client.PostAsync(url, content);
        if (response.IsSuccessStatusCode)
        {
            var responseContent = await response.Content.ReadAsStringAsync();
            return JsonConvert.DeserializeObject<dynamic>(responseContent).data.access_token;
        }
        else
        {
            Console.WriteLine($"Error: {response.StatusCode}");
            return null;
        }
    }


    static async Task CreateDeviceReq(string token)
    {
        var url = "http://localhost:4000/api/v1/devices";
        var deviceData = new
        {
            device = new { name = "New attempt dotnet linux" }
        };
        var data = JsonConvert.SerializeObject(deviceData);
        //var content = new StringContent(data, Encoding.UTF8, "application/json");
        //client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue(token);





        var request = new HttpRequestMessage(HttpMethod.Post, url);
        request.Headers.Add("Authorization", token);
        request.Headers.Add("User-Agent", "python-requests/2.31.0");
        request.Headers.Add("Accept", "*/*");
        request.Headers.Add("Accept-Encoding", "gzip, deflate, br");
        request.Headers.Add("Connection", "keep-alive");
        request.Content = new StringContent(data, Encoding.UTF8, "application/json");

        HttpResponseMessage response = await client.SendAsync(request);











        //Console.WriteLine($"{client.DefaultRequestHeaders}");
        //Console.WriteLine($"{client.Headers}");

        //var response = await client.PostAsync(url, content);
        //Console.WriteLine(response);
        if (response.IsSuccessStatusCode)
        {
            var responseContent = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseContent);
        }
        else
        {
            Console.WriteLine($"Error: {response.StatusCode}");
        }
    }


    static async Task CreateDevice(string token)
    {
        var url = "http://localhost:4000/api/v1/devices";
        var deviceData = new
        {
            device = new { name = "New attempt dotnet linux" }
        };
        var data = JsonConvert.SerializeObject(deviceData);
        var content = new StringContent(data, Encoding.UTF8, "application/json");
        client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue(token);
//        client.DefaultRequestHeaders.CacheControl = new System.Net.Http.Headers.CacheControlHeaderValue()
//        {
//            Public = true, // Makes the response cacheable by any cache
//            MustRevalidate = false
//        };

        Console.WriteLine($"{client.DefaultRequestHeaders}");
        //Console.WriteLine($"{client.Headers}");

        var response = await client.PostAsync(url, content);
        Console.WriteLine(response);
        if (response.IsSuccessStatusCode)
        {
            var responseContent = await response.Content.ReadAsStringAsync();
            Console.WriteLine(responseContent);
        }
        else
        {
            Console.WriteLine($"Error: {response.StatusCode}");
        }
    }
}

