from chassis.client import OMIClient

# Instantiate OMI Client connection to model running on localhost:45000
client = OMIClient("localhost", 45000)

# Call and view results of status RPC
status = await client.status()
print(f"Status: {status}")

# Submit inference with quickstart sample data
res = await client.run([{"input": "22133"}])

# Parse results from output item
result = res.outputs[0].output["results.json"]

# View results
print(f"Result: {result}")
