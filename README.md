# 📡 WireTapper

**Wireless OSINT & Signal Intelligence Platform**

WireTapper is a wireless OSINT tool designed to discover, map, and analyze radio-based devices using passive signal intelligence. It provides investigators, researchers, and security analysts with real-time visibility into the invisible wireless landscape around them.

WireTapper detects and correlates signals from common wireless technologies, helping users understand what devices exist, where they are likely located, and how they interact, without active intrusion.

🔗 **Website:** https://haybnz.web.app?utm_source=github.com
🔗 **Blog on WireTapper:** [https://haybnz.web.app/](https://medium.com/@h9z/wire-tapper-wireless-osint-signal-intelligence-platform-e5104659a1cb?utm_source=github.com)


## 📶 Supported Signal Intelligence

WireTapper can identify and analyze signals from:

*   **Wi-Fi** access points & clients
*   **Bluetooth & BLE** devices
*   **Wireless CCTV / IP cameras**
*   **Vehicles** broadcasting RF signals (infotainment, telemetry, keyless systems)
*   **Headphones, wearables**, and smart devices
*   **Smart TVs & IoT** appliances
*   **Cell towers** & mobile network beacons


## 🚀 Installation

Follow these steps to get WireTapper up and running:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/h9zdev/WireTapper.git
   cd WireTapper
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r WireTapper.txt
   ```

3. **Configure API Keys and Run:**

   Choose one of the following methods to configure your API keys and run the application:

   ### Method 1: Modify `app.py` (Direct Configuration)
   Open `app.py` and manually enter your API keys by replacing the empty strings:
   ```python
   WIGLE_API_NAME = "your_wigle_api_name"
   WIGLE_API_TOKEN = "your_wigle_api_token"
   OPENCELLID_API_KEY = "your_opencellid_api_key"
   SHODAN_API_KEY = "your_shodan_api_key"
   ```
   Then, start the server:
   ```bash
   python app.py
   ```

   ### Method 2: Use `app-env.py` (Environment Variables)
   This is the recommended approach for better security. You can export your keys in the terminal:
   ```bash
   export WIGLE_API_NAME="your_wigle_api_name"
   export WIGLE_API_TOKEN="your_wigle_api_token"
   export OPENCELLID_API_KEY="your_opencellid_api_key"
   export SHODAN_API_KEY="your_shodan_api_key"
   ```
   Alternatively, you can define these keys in a `.env` file. Then, start the server:
   ```bash
   python app-env.py
   ```

   The application will be available at `http://localhost:8080`.

## 📷 Screenshots

![WireTapper Image 1](https://raw.githubusercontent.com/h9zdev/WireTapper/main/images/Wiretapper11.png)  
![WireTapper Image 2](https://raw.githubusercontent.com/h9zdev/WireTapper/main/images/Wiretapper34.png)  
![WireTapper Image 3](https://raw.githubusercontent.com/h9zdev/WireTapper/main/images/Wiretapper354.png)  
![WireTapper Image 4](https://raw.githubusercontent.com/h9zdev/WireTapper/main/images/Wiretapper55.png)  
![WireTapper Image 5](https://raw.githubusercontent.com/h9zdev/WireTapper/main/images/Wiretapper568.png)


## 📜 License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License. See the [LICENSE](LICENSE) file for more details.

**Unauthorized use is strictly prohibited.**

📧 Contact: singularat@protn.me

## ☕ Support

Donate via Monero: `45PU6txuLxtFFcVP95qT2xXdg7eZzPsqFfbtZp5HTjLbPquDAugBKNSh1bJ76qmAWNGMBCKk4R1UCYqXxYwYfP2wTggZNhq`

## 👥 Contributors and Developers

[<img src="https://avatars.githubusercontent.com/u/67865621?s=64&v=4" width="64" height="64" alt="haybnzz">](https://github.com/h9zdev)  
