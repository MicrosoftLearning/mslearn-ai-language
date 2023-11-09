using System;
using System.IO;
using System.Text;
using Microsoft.Extensions.Configuration;

// Import namespaces
using Azure;
using Azure.AI.TextAnalytics;

namespace text_analysis
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
                string projectName = configuration["Project"];
                string deploymentName = configuration["Deployment"];

                // Create client using endpoint and key
                AzureKeyCredential credentials = new AzureKeyCredential(aiSvcKey);
                Uri endpoint = new Uri(aiSvcEndpoint);
                TextAnalyticsClient aiClient = new TextAnalyticsClient(endpoint, credentials);

                // Analyze each text file in the reviews folder
                List<string> batchedDocuments = new List<string>();
                
                var folderPath = Path.GetFullPath("./articles");  
                DirectoryInfo folder = new DirectoryInfo(folderPath);
                foreach (var file in folder.GetFiles("*.txt"))
                {
                    // Read the file contents
                    Console.WriteLine("\n-------------\n" + file.Name);
                    StreamReader sr = file.OpenText();
                    var text = sr.ReadToEnd();
                    sr.Close();
                    batchedDocuments.add(text);
                }

                // Get Classification
                ClassifyDocumentOperation operation = await aiclient.SingleLabelClassifyAsync(WaitUntil.Completed, batchedDocuments, projectName, deploymentName);

                // View the operation results.
                await foreach (ClassifyDocumentResultCollection documentsInPage in operation.Value)
                {
                    foreach (ClassifyDocumentResult documentResult in documentsInPage)
                    {
                        if (documentResult.HasError)
                        {
                            Console.WriteLine($"  Error!");
                            Console.WriteLine($"  Document error code: {documentResult.Error.ErrorCode}");
                            Console.WriteLine($"  Message: {documentResult.Error.Message}");
                            continue;
                        }

                        Console.WriteLine($"  Predicted the following class:");
                        Console.WriteLine();

                        foreach (ClassificationCategory classification in documentResult.ClassificationCategories)
                        {
                            Console.WriteLine($"  Category: {classification.Category}");
                            Console.WriteLine($"  Confidence score: {classification.ConfidenceScore}");
                            Console.WriteLine();
                        }
                    }
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }



    }
}
