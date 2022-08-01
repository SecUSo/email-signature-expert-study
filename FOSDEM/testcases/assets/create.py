#!/usr/bin/env python

from email.message import Message
from email import message_from_file

mail = Message()
mail.add_header("To", "alice@securepay24.de")
mail.add_header("From", "bob@code-audit.org")
mail.add_header("Subject", "Upcoming Security Audit")
mail.add_header("Message-ID", "<58b67214-dfee-d98b-b74e-2e04a334b71c@securepay24.de>")
mail.add_header("Date", "Sat, 01 Feb 2020 12:34:56 +0200")
mail.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101\r\n Thunderbird/68.4.2")
mail.add_header("MIME-Version", "1.0")
mail.add_header("Content-type", "multipart/signed", micalg="pgp-sha256", protocol="application/pgp-signature")

part_text = message_from_file(open("text.txt"))

part_sign = Message()
part_sign.add_header("Content-Type", 'application/pgp-signature; name="signature.asc"')
part_sign.add_header("Content-Description", "OpenPGP digital signature")
part_sign.add_header("Content-Disposition", "attachement", filename="signature.asc")
sign = open("text.txt.asc", "rt").read()
part_sign.set_payload(sign)

mail.set_payload([part_text, part_sign])

print(str(mail))

print(r"WARNING: this script has a bug and does not work under Linux as intended. You need to replace all '\n' with '\r\n' in the eml body after the mail was generated. Otherwise the signature is broken.")

res = str(mail).encode("ascii").replace(b"\n", b"\r\n")

open("text.eml", "wb").write(res)

#open("test.eml", "wt").write(str(mail))
