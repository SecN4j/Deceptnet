import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

log_path = Path("cowrie.json")

events = []
with open(log_path, "r") as f:
    for line in f:
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

df = pd.DataFrame(events)
df['timestamp'] = pd.to_datetime(df['timestamp'])
print(f"\nData spans from {df['timestamp'].min()} to {df['timestamp'].max()}")

print(f"Total events loaded: {len(df)}")
print(f"Event types found:\n{df['eventid'].value_counts()}")
logins = df[df['eventid'].isin(['cowrie.login.success', 'cowrie.login.failed'])].copy()
logins['result'] = logins['eventid'].apply(lambda x: 'Success' if 'success' in x else 'Failed')

print("\n Login Summary ")
print(logins['result'].value_counts())

print("\n Top attempted usernames ")
print(logins['username'].value_counts().head(10))

print("\n Top attempted passwords ")
print(logins['password'].value_counts().head(10))

result_counts = logins['result'].value_counts()
plt.figure(figsize=(6,4))
result_counts.plot(kind='bar', color=['#4CAF50' if x == 'Success' else '#F44336' for x in result_counts.index])
plt.title('Login Attempts: Success vs Failed')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('/home/deceptnet/login_success_vs_failed.png')
print("\nChart saved: login_success_vs_failed.png")

# Command Frequency Analysis 
def analyze_command_frequency(df):
    cmd_events = df[df['eventid'] == 'cowrie.command.input'].copy()
    if cmd_events.empty:
        print("\nNo command.input events found.")
        return

    all_commands = []
    for raw in cmd_events['input'].dropna():
        commands = [cmd.strip() for cmd in raw.split(';')]
        all_commands.extend([cmd for cmd in commands if cmd])

    cmd_series = pd.Series(all_commands)
    cmd_counts = cmd_series.value_counts()

    print(f"\nTotal command executions captured: {len(all_commands)}")
    print(f"Unique commands: {cmd_counts.nunique()}")
    print("\nCommand frequency:")
    print(cmd_counts)

    plt.figure(figsize=(10, 5))
    cmd_counts.plot(kind='bar', color='#E53935')
    plt.title('Attacker Command Frequency (Post-Compromise Session)')
    plt.xlabel('Command')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('/home/deceptnet/command_frequency.png')
    print("\nChart saved: command_frequency.png")

analyze_command_frequency(df)
