using System;
using System.IO;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;
using System.Threading.Tasks;

// import namespaces



namespace custom_entities
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


                // Read each text file in the ads folder
                List<TextDocumentInput> batchedDocuments = new();              
                var folderPath = Path.GetFullPath("./ads");  
                DirectoryInfo folder = new(folderPath);
                FileInfo[] files = folder.GetFiles("*.txt");
                foreach (var file in files)
                {
                    // Read the file contents
                    StreamReader sr = file.OpenText();
                    var text = sr.ReadToEnd();
                    sr.Close();
                    TextDocumentInput doc = new(file.Name, text)
                    {
                        Language = "en",
                    };
                    batchedDocuments.Add(doc);
                }

                // Extract entities



            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }



    }
}
