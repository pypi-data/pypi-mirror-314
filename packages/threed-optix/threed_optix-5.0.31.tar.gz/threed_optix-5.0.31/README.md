# What is 3DOptix?

## The fastest, most intuitive, non-sequential, ray tracing, cloud-based, optical system simulation software.

3DOptix’s innovative GPU and cloud-based ray tracing engine can trace billions of rays per second, faster than any other simulation software on the market.
Our easy-to-use application enables you to easily design both simple and complex optical systems and make smart decisions based on real data.
3DOptix Warehouse is the first ever cloud-based workspace for sharing optical designs. With numerous designs available, the 3DOptix Warehouse offers engineers an unparalleled resource for exploring new ideas, discovering innovative solutions, and finding great starting points for their own designs.

# Optical Simulation SDK

Our SDK is released in a beta version and has only limited features support at the moment.
We are working on supporting more features and you can expect new versions to come out soon.

Complete manual can be found in 3DOptix application:
https://simulation.3doptix.com/ > "help" > "API"

## Installation

3DOptix python package installation is available using PyPi:

```bash
pip install threed-optix
```

## Usage

```python
import threed_optix as tdo

#Your API key from 3DOptix user interface
api_key = '<your_api_key>'

#api is the object that manages the communication with 3DOptix systems
api = tdo.Client(api_key)

```

> **Note**
> The rest of the usage instructions can be found in 3DOptix simulation interface under "Help > API"

## Get Your API Key

Get your API key from 3DOptix user interface (under "user settings"):

- Click on your email, and choose **"user settings"** in the drop-down
  ![User settings](https://i.yourimageshare.com/MyBdTqNzyQ.webp "User settings")
- On the buttom of the settings manu, click on **"API"**
  ![API settings](https://i.yourimageshare.com/IbcB26QfJh.webp "API settings")
- **Copy** your API key
  ![Get API key](https://i.yourimageshare.com/tPq7LC8Qfy.webp "Get API key")

# License

3DOptix API is available with [MIT License](https://choosealicense.com/licenses/mit/).
