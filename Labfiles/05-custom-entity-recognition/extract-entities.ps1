# Update these with your service and model values
$key="<YOUR-KEY>"
$endpoint="<YOUR-ENDPOINT>"
$projectName = "customNERLab"
$modelName = "customExtractAds"
$verbose = $false

# Set up headers for API call
$headers = @{}
$headers.add("Ocp-Apim-Subscription-Key", $key)
$headers.add("Content-Type","application/json")

# Get text to extract entities from
$text_file = "test1.txt"
if ($args.count -gt 0)
{
    $text_file = $args[0]
}

try {
    $contents = get-content $text_file -raw -ErrorAction Stop
}
catch {
    Write-Host "`nError reading provided file, please verify file exists`n"
    Exit
}

# Build body of for API call
$data = @{
    "tasks" = @{
        "customEntityRecognitionTasks" = @(
            @{
                "parameters"= @{
                      "project-name" = $projectName
                      "deployment-name" = $modelName
                }
            }
        )
    }
    "analysisInput" = @{
        "documents" = @(
            @{
                "id" = "document_extractEntities"
                "text" = $contents
            }
        )
    }
} | ConvertTo-Json -Depth 6

# Post text for entity recognition
Write-Host("`nSubmitting entity recognition task`n")
$response = Invoke-WebRequest -Method Post `
          -Uri "$($endpoint)text/analytics/v3.2-preview.2/analyze" `
          -Headers $headers `
          -Body $data

# Output response if desired
if ($verbose) {
    Write-Host("`nResponse header:$($response.Headers['Operation-Location'])`n")
}

# Extract the URL from the response
# to call the API to getting the analysis results
$resultUrl = $($response.Headers['Operation-Location'])

# Create the header for the REST GET with only the subscription key
$resultHeaders = @{}
$resultHeaders.Add( "Ocp-Apim-Subscription-Key", $key )

# Get the results
# Continue to request results until the analysis is "succeeded"
Write-Host "Getting results..."
Do {
    $result = Invoke-RestMethod -Method Get `
            -Uri $resultUrl `
            -Headers $resultHeaders | ConvertTo-Json -Depth 10

    $analysis = ($result | ConvertFrom-Json)
} while ($analysis.status -ne "succeeded")
Write-Host "...Done`n"

# Access the relevant fields from the analysis
$extraction = $result | ConvertFrom-Json
$docs = $extraction.tasks.customEntityRecognitionTasks[0].results.documents

# Output response if desired
if ($verbose) {
    Write-Host("GET JSON Response:`n$result`n")
}

for (($idx = 0); $idx -lt $docs.Length; $idx++) {
    $item = $docs[$idx] 
    Write-Host ("Document #", ($idx+1))
    $entities = $item.entities
    foreach ($entity in $entities) {
        Write-Host ("  - Entity Category: $($entity.category)")
        Write-Host ("  - Entity Text:  $($entity.text)")
        Write-Host ("  - Confidence:  $($entity.confidenceScore)`n")
    }
    
}
