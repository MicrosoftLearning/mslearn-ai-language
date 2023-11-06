using System;
using System.IO;
using System.Text;
using Microsoft.Extensions.Configuration;

// Import namespaces


namespace qna_app
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string aiSvcEndpoint = configuration["AIServicesEndpoint"];
                string aiSvcKey = configuration["AIServicesKey"];
                string projectName = configuration["QAProjectName"];
                string deploymentName = configuration["QADeploymentName"];

                // Create client using endpoint and key


                // Submit a question and display the answer
                

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }



    }
}
