using System;
using Azure;
using System.IO;
using System.Text;
using System.Collections.Generic;
using Microsoft.Extensions.Configuration;

// Add references


namespace chat_app
{
    class Program
    {
        static void Main(string[] args)
        {
            // Clear the console
            Console.Clear();
            
            try
            {
                // Get configuration settings
                IConfigurationBuilder builder = new ConfigurationBuilder().AddJsonFile("appsettings.json");
                IConfigurationRoot configuration = builder.Build();
                string project_connection = configuration["PROJECT_ENDPOINT"];
                string model_deployment = configuration["MODEL_DEPLOYMENT"];



                // Initialize the project client



                // Get a chat client




                // Initialize prompts
                string system_message = "You are an AI assistant for a produce supplier company.";
                string prompt = "";

                // Loop until the user types 'quit'
                while (prompt.ToLower() != "quit")
                {
                    // Get user input
                    Console.WriteLine("\nAsk a question about the audio\n(or type 'quit' to exit)\n");
                    prompt = Console.ReadLine().ToLower();
                    if (prompt == "quit")
                    {
                        break;
                    }
                    else if (prompt.Length < 1)
                    {
                        Console.WriteLine("Please enter a question.\n");
                        continue;
                    }
                    else
                    {
                        Console.WriteLine("Getting a response ...\n");


                        // Get a response to audio input
                        

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