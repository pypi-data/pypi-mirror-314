# Femtum SDK - Dotnet

[![NuGet](https://img.shields.io/nuget/v/Femtum.SDK.svg)](https://www.nuget.org/packages/Femtum.SDK)

### Installation

To install the Femtum SDK, use the following command:

##### pip

```bash
pip install femtum-sdk
```

##### poetry

```bash
poetry add femtum-sdk
```

### Usage

Here is a basic example of how to use the Femtum SDK:

1. Start the SDK Server
2. Use SDK in your code

```python
with FemtumSdk() as sdk:
  request = FindResultDataRequestDto()
  result: OpticalSpectralAnalyserSweepResultDtoArray = (
      sdk.analysis.FindOpticalSpectralAnalyserSweepResults(request)
  )

  print(result.Items)
```

or

```python

sdk = FemtumSdk()

request = FindResultDataRequestDto()
result: OpticalSpectralAnalyserSweepResultDtoArray = (
    sdk.analysis.FindOpticalSpectralAnalyserSweepResults(request)
)

print(result.Items)

sdk.close()
```

#### With Specified SDK server url

```python
with FemtumSdk(hostUrl=api_server.get_grpc_url()) as sdk:
  request = FindResultDataRequestDto()
  result: OpticalSpectralAnalyserSweepResultDtoArray = (
      sdk.analysis.FindOpticalSpectralAnalyserSweepResults(request)
  )

  print(result.Items)
```
