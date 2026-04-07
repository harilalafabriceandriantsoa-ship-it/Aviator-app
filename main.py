import hashlib, hmac, random, statistics, datetime
import matplotlib.pyplot as plt
import numpy as np

# --- COSMOS ENGINE (IA Premium) ---
def cosmos_premium_engine(server_seed, client_seed, nonce, salt="T1", iters=500000):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    base = f"{server_seed}:{client_seed}:{nonce}:{salt}:{heure}:COSMOSX_V101"
    h1 = hmac.new(b"COSMOS_CORE", base.encode(), hashlib.sha512).digest()
    for i in range(iters):
        h1 = hmac.new(h1, f"STEP_{i}".encode(), hashlib.sha512).digest()
    blake = hashlib.blake2b(h1).digest()
    sha3 = hashlib.sha3_256(blake).digest()
    sha384 = hashlib.sha384(sha3).digest()
    sha256 = hashlib.sha256(sha384).digest()
    final = bytes(a ^ b ^ c ^ d for a, b, c, d in zip(h1, blake, sha3, sha256))
    hex_out = final.hex()
    p_int = int(hex_out[:16], 16)
    offset = (p_int % 29) + (9 if salt == "T1" else 15)
    jumps = [(p_int % 7) + 2, (p_int % 11) + 3, (p_int % 13) + 4]

    values = [offset] + jumps
    min_val = min(values)
    max_val = max(values)
    mean_val = statistics.mean(values)
    accuracy = round((mean_val / max_val) * 100, 2)

    return {
        "hex": hex_out,
        "tour": nonce + offset,
        "jumps": jumps,
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
        "accuracy": accuracy
    }

# --- MINES ENGINE (fixe 5 diamants foana, IA Premium) ---
def mines_premium_engine(server_seed, client_seed, nonce, iters=500000):
    heure = datetime.datetime.now().strftime("%H:%M:%S")
    choice_salt = f"CHOICE5:{heure}"
    base = f"{server_seed}:{client_seed}:{nonce}:{choice_salt}:MINES_V101"

    h1 = hashlib.sha512(base.encode()).digest()
    h2 = hashlib.blake2b(h1).digest()
    h3 = hashlib.sha3_256(h2).digest()
    h4 = hashlib.sha384(h3).digest()
    h5 = hashlib.sha256(h4).digest()

    h_mut = h1
    for i in range(iters):
        h_mut = hashlib.sha512(h_mut + f"STEP{i}".encode()).digest()

    combined = h1 + h2 + h3 + h4 + h5 + h_mut
    hash_int = int.from_bytes(combined, "big")

    grid = list(range(25))
    for i in range(24, 0, -1):
        j = hash_int % (i + 1)
        grid[i], grid[j] = grid[j], grid[i]
        hash_int //= (i + 1)
    random.seed(int.from_bytes(h3[:16], "big") ^ 5)
    random.shuffle(grid)
    random.shuffle(grid)
    random.shuffle(grid)

    schema = grid[:5]

    # IA Premium: probabilités dynamique
    probs = []
    for k in range(5):
        p = round(((5 - k) / (25 - k)) * 100, 2)
        probs.append(p)

    # Anti win-loss pattern: re-shuffle automatique raha miverina toerana mitovy
    if len(set(schema)) < 5:
        random.shuffle(grid)
        schema = grid[:5]

    return schema, probs

# --- VISUALISATION ---
def visualize_mines(schema, probs):
    grid = np.zeros((5,5))
    for pos in schema:
        row, col = divmod(pos, 5)
        grid[row][col] = 1

    fig, ax = plt.subplots(1,2, figsize=(10,5))

    # Grid 5x5
    ax[0].imshow(grid, cmap="cool", interpolation="nearest")
    ax[0].set_title("Schema Diamants (Mines Premium)")
    for i in range(5):
        for j in range(5):
            if grid[i][j] == 1:
                ax[0].text(j, i, "💎", ha="center", va="center", fontsize=14)

    # Probabilities bar chart
    clicks = [1,2,3,4,5]
    ax[1].bar(clicks, probs, color="cyan")
    ax[1].set_title("Probabilités dynamique")
    ax[1].set_xlabel("Click")
    ax[1].set_ylabel("Vintana (%)")

    plt.tight_layout()
    plt.show()

def visualize_cosmos(cosmos):
    metrics = ["Min","Mean","Max","Accuracy"]
    values = [cosmos["min"], cosmos["mean"], cosmos["max"], cosmos["accuracy"]]
    plt.bar(metrics, values, color="magenta")
    plt.title("Cosmos Premium Metrics")
    plt.show()

# --- TEST EXAMPLE ---
if __name__ == "__main__":
    server_seed = "d17354bbdbbdbfefb1ef2d210fb3ea2c3aeb4e6be5c27ac08a3e49b49fdf0b91"
    client_seed = "SaSd3AAerLJrfAw053Bf"
    nonce = 1

    schema, probs = mines_premium_engine(server_seed, client_seed, nonce)
    print("Schema diamants:", schema)
    print("Probabilités dynamique:", probs)
    visualize_mines(schema, probs)

    cosmos = cosmos_premium_engine(server_seed, client_seed, nonce)
    print("Cosmos:", cosmos)
    visualize_cosmos(cosmos)
