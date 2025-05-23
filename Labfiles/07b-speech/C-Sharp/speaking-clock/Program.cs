﻿using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

// Import namespaces


namespace speaking_clock
{
    class Program
    {
        private static SpeechConfig speechConfig;

        static async Task Main(string[] args)
        {

            // Clear the console
            Console.Clear();

            try
            {
                // Get config settings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string projectKey = configuration["PROJECT_KEY"];
                string location = configuration["LOCATION"];

                // Configure speech service


                // Get spoken input
                string command = "";
                command = await TranscribeCommand();
                if (command.ToLower()=="what time is it?")
                {
                    await TellTime();
                }

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        static async Task<string> TranscribeCommand()
        {
            string command = "";
            
            // Configure speech recognition


            // Process speech input


            // Return the command
            return command;
        }

        static async Task TellTime()
        {
            var now = DateTime.Now;
            string responseText = "The time is " + now.Hour.ToString() + ":" + now.Minute.ToString("D2");
                        
            // Configure speech synthesis


            // Synthesize spoken output


            // Print the response
            Console.WriteLine(responseText);
        }

    }
}
