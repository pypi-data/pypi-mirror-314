from byterat.client import ByteratClientSync

# Replace with API_KEY
API_TOKEN = "af67a26f5172d047d9cad57a59a58213587f1850e20c3f5a163399c38290f26470499aec994a34a00a915941af1a8422"


def main():
    client = ByteratClientSync(API_TOKEN)

    # Up to 100 entries are returned in one go by default.
    continuation_token = None
    while True:
        resp = client.get_observation_metrics_by_dataset_key(
            "B14B-6", continuation_token
        )
        continuation_token = resp.continuation_token
        if not continuation_token:
            break

        print(resp.data)


if __name__ == "__main__":
    main()
