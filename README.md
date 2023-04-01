# temp-mail-python

`temp-mail-python` is a Python wrapper for Temp Mail API. Temp Mail API is a free and secure temporary email service that allows you to receive emails at a temporary address that will self-destruct after a certain period of time. This wrapper library provides an easy-to-use interface for interacting with the Temp Mail API and allows you to create, read and delete temporary emails.

## Prerequisites
Create a free APILayer account [here](https://apilayer.com/signup) and subscribe to the [Temp Mail API](https://apilayer.com/marketplace/temp_mail-api). You will receive an API key that you can use with this wrapper library.

## Installation

You can install `temp-mail-python` using pip:

```bash
pip install git+https://github.com/krishna2206/temp-mail-python.git
```

## Usage

Import the `TempMail` class from `temp-mail-python` and initialize it with your Temp Mail API key:

```python
from tempmail import TempMail

tm = TempMail(api_key='YOUR_API_KEY_HERE')
```

## Examples

### Get list of usable domains

```python
domains = tm.get_domains()
print(domains)
```

### Create a temporary email address

You can either create a temporary email address with a random username or specify a username of your choice.

```python
# Create a temporary email address with a random username
email = tm.create_email()
print(email)

# Create a temporary email address with a specified username
email = tm.create_email(username='example')
print(email)
```

### Get list of emails for an email address

```python
emails = tm.get_emails('example@example.com')
print(emails)
```

### Get one email message by id

```python
email = tm.get_email('email_id')
print(email)
```

### Get message attachments by email id

```python
attachments = tm.get_attachments('email_id')
print(attachments)
```

### Get one message attachment by email id and attachment id

```python
attachment = tm.get_one_attachment('email_id', 'attachment_id')
print(attachment)
```

### Delete email message by id

```python
response = tm.delete_email('email_id')
print(response)
```

## License

MIT License

Copyright (c) 2023 Anhy Krishna Fitiavana

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED,
