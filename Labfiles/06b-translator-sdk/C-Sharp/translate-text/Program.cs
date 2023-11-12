using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using Microsoft.Extensions.Configuration;
using System.Threading.Tasks;

// Import namespaces


namespace translate_text
{
    class Program
    {
        static async Task Main(string[] args)
        {
            try
            {
                // Set console encoding to unicode
                Console.InputEncoding = Encoding.Unicode;
                Console.OutputEncoding = Encoding.Unicode;

                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string translatorRegion = configuration["TranslatorRegion"];
                string translatorKey = configuration["TranslatorKey"];

                // Choose target language
                string targetLanguage = "xx";
                var languages = new List<string> {"en", "fr", "es", "hi", "ja", "ru"};
                while (!languages.Contains(targetLanguage))
                {
                    Console.WriteLine("Choose a target language.");
                    foreach (string language in languages)
                    {
                        Console.Write(language + " ");
                    }
                    Console.WriteLine(":");
                    targetLanguage = Console.ReadLine();
                }



                // Create client using endpoint and key



                // Translate text

                

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }



    }
}
