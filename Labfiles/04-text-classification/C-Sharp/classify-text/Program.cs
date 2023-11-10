using System;
using System.IO;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;
using System.Threading.Tasks;

// Import namespaces


namespace classify_text
{
    class Program
    {
        static async Task Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string aiSvcEndpoint = configuration["AIServicesEndpoint"];
                string aiSvcKey = configuration["AIServicesKey"];
                string projectName = configuration["Project"];
                string deploymentName = configuration["Deployment"];

                // Create client using endpoint and key


                // Read each text file in the articles folder
                List<string> batchedDocuments = new List<string>();
                
                var folderPath = Path.GetFullPath("./articles");  
                DirectoryInfo folder = new DirectoryInfo(folderPath);
                FileInfo[] files = folder.GetFiles("*.txt");
                foreach (var file in files)
                {
                    // Read the file contents
                    StreamReader sr = file.OpenText();
                    var text = sr.ReadToEnd();
                    sr.Close();
                    batchedDocuments.Add(text);
                }

                // Get Classifications


            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }



    }
}
