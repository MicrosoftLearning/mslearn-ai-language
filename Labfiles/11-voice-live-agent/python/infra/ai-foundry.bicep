@description('Primary location for all resources')
param location string

@description('Name of the environment used to derive resource names')
param environmentName string

@description('Unique token for resource naming')
param resourceToken string

@description('Tags to apply to resources')
param tags object = {}

@description('Principal ID for role assignments')
param principalId string

// Create AI Foundry resource (modern approach - no separate project needed for model deployment)
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: 'ai-foundry-${resourceToken}'
  location: location
  tags: union(tags, {
    'azd-service-name': 'gpt-realtime-model'
  })
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: 'ai-foundry-${resourceToken}'
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
}

// Deploy GPT Realtime model directly to AI Foundry
resource gptRealtimeDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: aiFoundry
  name: 'gpt-4o'
  sku: {
    name: 'GlobalStandard'
    capacity: 1
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-11-20'
    }
    raiPolicyName: 'Microsoft.Default'
  }
}

// Role assignment for the user to access AI Foundry
resource cognitiveServicesOpenAIUser 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  scope: subscription()
  name: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd' // Cognitive Services OpenAI User
}

resource aiFoundryRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: aiFoundry
  name: guid(aiFoundry.id, principalId, cognitiveServicesOpenAIUser.id)
  properties: {
    roleDefinitionId: cognitiveServicesOpenAIUser.id
    principalId: principalId
    principalType: 'User'
  }
}

// Outputs
output endpoint string = aiFoundry.properties.endpoint
output apiKey string = aiFoundry.listKeys().key1
output realtimeModelName string = gptRealtimeDeployment.name
output foundryName string = aiFoundry.name