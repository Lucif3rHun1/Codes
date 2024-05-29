import tls_client

session = tls_client.Session(
        client_identifier="chrome112",
        random_tls_extension_order=True
    )
print(session.post("https://www.betmgm.com/en/mobileportal/api/Registration/CheckEmailAddress").text)