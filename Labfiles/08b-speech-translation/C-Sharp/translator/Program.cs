using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using System.Collections.Generic;
using System.Text;

// Import namespaces


namespace speech_translation
{
    class Program
    {
        private static SpeechConfig speechConfig;
        private static SpeechTranslationConfig translationConfig;

        static async Task Main(string[] args)
        {
            try
            {
                // Get config settings from AppSettings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string projectKey = configuration["PROJECT_KEY"];
                string location = configuration["LOCATION"];

                // Set console encoding to UTF-8
                Console.InputEncoding = Encoding.UTF8;
                Console.OutputEncoding = Encoding.UTF8;

                // Configure translation


                // Configure speech
                

                string targetLanguage = "";
                while (targetLanguage != "quit")
                {
                    Console.WriteLine("\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n");
                    targetLanguage=Console.ReadLine().ToLower();
                    if (translationConfig.TargetLanguages.Contains(targetLanguage))
                    {
                        await Translate(targetLanguage);
                    }
                    else
                    {
                        targetLanguage = "quit";
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task Translate(string targetLanguage)
        {
            string translation = "";

            // Translate speech


            // Synthesize translation


        }

    }
}
