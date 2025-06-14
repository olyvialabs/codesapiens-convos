from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CELERY_BROKER_URL: str  # = "redis://:AVNS_oNKZNl-3XYll-hf4wC7@db-redis-nyc3-02239-do-user-12860484-0.c.db.ondigitalocean.com:25061/codesapiens0"
    # = "redis://:AVNS_oNKZNl-3XYll-hf4wC7@db-redis-nyc3-02239-do-user-12860484-0.c.db.ondigitalocean.com:25061/codesapiens1"
    CELERY_RESULT_BACKEND: str
    OPENAI_API_KEY: str = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"  # can be gpt4
    output_folder: str = "outputs"
    temp_folder: str = "temp"
    SUPABASE_URL: str = None
    SUPABASE_KEY: str = None
    CROSS_ORIGIN_SERVICE_SECRET: str = None
    MONOLITH_URL: str = None
    GITHUB_APP_ID_NUMBER: str = None
    GITHUB_APP_PRIVATE_KEY_BASE64: str = 'LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb2dJQkFBS0NBUUVBek82K040K0J2V1ZwVXI0MktVQmxYRHcxMDRlOFdRT0EwbzgvNFNzcXpWTlM4WnBGCmMwa0hKVzFtdlhSdG8vQWZzNjdiQ1FWeEVTaXR4Zlo2RVI5eGJKT1czMGtHZnFQVmc4UHh3cHhQWWlSbE11Y2UKWmRVZTBJNGRwQWVSQThJaFRheWJnK1ovS2E4T0EveXJjT05CV2RzdVNjUmVoaCt0OVJYQkdsQUxPQlUvSS9BawpSSnRDa0V1VkYzL1NTdXFWWUI3Y3R0K1g2YnJQTkhYdTlRczdDZmtOVlFkOUJwVFIyeDNpVmJscjFUMUFpajVZCkMweGRveVdsWWxyakRkQVIycHM4Z0F2UW1sN04xcm4xbVhJQ0NBZHRYUTMxZmNZTGgzSHZYYjB6aFF2dUVKYWgKMFJxcUNIcUtmMytYNXlzNUFnTnVwMVVEZHQ2QjdaM1o0TWYvQndJREFRQUJBb0lCQUFqYU8wOU5ISzZneGRiMApMb1REcWwwOG9KcWRuMjQ4NzRDby9YcHRrZkRDcTYrU0dYUHNjS21XT3p6dDNacWFVZFJDTm1ZQ1hTci9sZG9hClZwV014U3FLaVpibG9ha3d6SlZmam43NG41ayt0enhtclhKNnJWVVcvb0xLYk9JN3JaS2NaUzlpY3BYTFlSQ2QKQm83ZTBrRGViZlp6ekIyQkd0T2VkL1A2QnpJSjdSUnY2YkdqWXNRMi9XUStnMjFCdWc5QVFpbm9iNmlCaWozUgpHc1dWTjFwSStXZ0ZvNkUvMVpWcVkwbnpFTEYwcGJvbzZpSk9VaEZyTXRKMi9FZHUvcXI2RjljaHI0M0Jma3lOCkxhYnBtTEpBSDFhUCtESUk3YmwrNy9LSGprQVcxYXc3MVFSY3Fva3EvbGo3RUMycGFkcnR4YUMyUUkwYU1MZ0IKOXUyaW1Ba0NnWUVBOWcwalJweUNyUDEyVFR4NmI4dnYydnozMUpjWEc1MUxuRTdSMmJnNi83a21WeVNRQlBtOAozMVhLT3c3ZUU2ZmNqWVc0ODgxY0R4eXZYQjBnazNXcGR0eEt1MW5BTVNxc1I0RFF6N2FwczBSNS9ReTlUc2trCkdrcENOL2xySm01Qi8vR2NXRlNTMkpmajkvQm1CdWpyK29QNlpTbno4ODR5YTNJcUNpcXIwcDBDZ1lFQTFUZjgKM3ZhVWJ1Z2cwcnNiMXlzTWczLzRWV3l1d01IaHMrZVpXL3JrbFcwd0Q0Z3RXWllTQkUvNktESWQ3bXVtdzVWVAo1clZ4VUJZSlk4dk5HUWRhREtuSlZRQXRpZmNRSExaYWhvdG9OLzF4UXpnTmZFdDBURm41RHVJbVpRUStWTzVJCk5ucXBBNlJhN3lpeTZyalY4SnAybGJMc1M2dXVBTU1DVkswRkpQTUNnWUJTbUxadXpidFFOd1d2aDgzU0diTzYKMzVDU1hPWDA3eWlpb0JMeDgxWmE0ZHh0QkdrVVFvR1V0MGZiNjNIQlIyaFNXY0ZzbGxPQS96QWV5K2hUbC92NwpXcGY3ckhWSUMvc3BSYVRURlk2Q0QwcWtGOUswei9DK29vNzRHMUpNNUZaamhNZm5IdnpzbUpCK2VzVEZMUXVLClhTT0JNa1FpWStXcEMvbnd6OEkrUVFLQmdIVHBTU2Q4YnpGTTZNcUR2Q1ZFUG8xUU92dWtKMEljVFVUWEpma1EKWGd3dEhhQTJuQjgyTVZUYUFhSE9zU2pOTUZpbjVhUm9NdVNsNEtvdTBwdjVzditralhlbExGTXMvRkd5RDNzYwpyNTJidzJJSE55WERQZGFyc3V2ZFJ3NDJ3SExUWVJjMk5MeUJmemNKeXVqM1JwK3lJbm04N09JbEZiam5OTHozClRnM1BBb0dBSU9yVGJvT1gzZVJidG5VYWNCeFArdHhaSkFxbll0dVY0NWdFZmhLNnEzUUR1TXZhUzgzRncwckkKQVhyeDFVYUtkZGlleG1zNHJNZVpiSVIwMFVSUlFMek1tRnFBRTluTFRJZzZ5am9YNTVreVBTcDRtbFpMSFhvZApFSFQzaThYUHhBY3NtWG5hUFRqZUVIYjh4MlFob2QweFRWL2dicWFwTDcrUmdiUi8wYU09Ci0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg=='


path = Path(__file__).parent.parent.absolute()
settings = Settings(_env_file=path.joinpath(
    ".env"), _env_file_encoding="utf-8")
