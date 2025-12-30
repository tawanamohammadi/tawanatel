# Tawana Telecom Bot (TTC)

A professional Telegram bot for selling virtual numbers, designed for high-performance and scalability. TTC operates as an independent, anonymous operator providing reliable SMS activation services.

## Repository
[https://github.com/tawanamohammadi/tawanatel](https://github.com/tawanamohammadi/tawanatel)

## Features
- 📱 Buy virtual numbers for top services (Telegram, WhatsApp, Google, etc.)
- 🌍 Global coverage with support for multiple countries.
- 💰 Secure wallet system with admin-managed balance.
- 🛠 Comprehensive Admin Panel for user and balance management.
- 🔄 Automated workflows: Real-time SMS monitoring and instant refunds on cancellations.
- 🚀 Optimized for Ubuntu 22.04.

## Installation (Ubuntu 22.04)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tawanamohammadi/tawanatel.git
   cd tawanatel
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot:**
   Update `config.py` or create a `.env` file with your credentials:
   - `BOT_TOKEN`: Your Telegram bot token (from @BotFather)
   - `TTC_API_KEY`: Your TTC API key
   - `ADMIN_IDS`: List of Telegram user IDs for admins

4. **Run the bot:**
   ```bash
   python3 main.py
   ```

## Deployment with Systemd

1. Copy `tawanatel.service` to `/etc/systemd/system/`:
   ```bash
   cp tawanatel.service /etc/systemd/system/
   ```

2. Edit the service file to match your environment:
   ```bash
   nano /etc/systemd/system/tawanatel.service
   ```

3. Start and enable the service:
   ```bash
   systemctl daemon-reload
   systemctl start tawanatel
   systemctl enable tawanatel
   ```

## API Protocol
TTC follows a robust API protocol compatible with standard SMS activation services. Documentation can be found in the `API protocol` directory.
