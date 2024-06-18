# eMinuto

eMinuto is a free and open-source software (FOSS) for a self-created, decentralized, trust-based digital means of payment.

It is based on the idea of [Minuto Cash](https://minuto.org/), a time voucher currency that can be self-issued. Each issued  Minuto voucher is secured by two guarantors. A voucher of 60 Minuto is worth 60 minutes of quality work.

## Why eMinuto?

Creating your own currency independent of institutions is appealing. As a natural progression, eMinuto continues many of the features of Minuto Cash, such as:

- Decentralized, usable in a similar way to cash, stable value, trust and meaning-based. 
- Can be created independently (no need for fiat money, electricity, etc.). 
- Unobtrusive, introducing a new money paradigm (human value-based). 
- Ideal medium of exchange (no incentives for speculation). 
- Less hype due to stable value (no price surges attracting speculators).

eMinuto caters to the digital age, providing an alternative for those who avoid cash. Businesses and freelancers typically make transactions via bank transfers rather than cash.

While the use of paper vouchers of Minuto Cash is mostly tied to a region, eMinuto can be used by trust-based networks over longer distances via Internet.

Unlike cryptocurrencies often used for speculation, eMinuto is designed solely as a medium of exchange, ensuring value creation.

## How it works

The eMinuto prototype uses text files that contain a transaction list (= a mini blockchain). Instead of anonymous addresses, known user IDs are used. These text files are digitally signed by the creator and guarantors using their user IDs.

eMinuto files can be sent to other users, with digital signatures in the transaction list confirming ownership. A global blockchain is unnecessary (serverless).

Fraud detection (e.g. double spending) relies on social control and the high probability of detection and post-factum proof. Being excluded from the trusted network is a significant social penalty.

For a detailed presentation about eMinuto, visit [eminuto.org](https://eminuto.org).

## Screenshots

<img src="https://github.com/minutogit/eMinuto-Desktop-Prototype/assets/113858632/bac4b98c-c827-4a44-81c8-fba2608f0177" alt="mainwindow" width="250px"> <img src="https://github.com/minutogit/eMinuto-Desktop-Prototype/assets/113858632/2f745f39-ad88-487c-9496-87e7ad2ae77e" alt="profile" width="200px">

## Features

- User profile
- Issue and send eMinuto vouchers.
- Import vouchers into the wallet
- Transaction list and voucher list showing own and others' vouchers and their values. 
- Privacy: Transactions and voucher files are encrypted.
- Raw voucher data can be viewed in the GUI.
- New: Languages of GUI: English, German
- Note: The prototype does not yet warn about detected double spending.

## Installation / Usage

### Windows

Download the latest release, unzip, and run `eMinuto.exe`. The file is unsigned and will be flagged as untrusted by Windows. Disable Windows Defender to run it.

### Linux

Download the latest release, unzip, right-click the `eMinuto` file, make it executable in the permissions and double-click it to start it. 

If it fails to start, run it in the terminal and check for error messages:

`/path/to/eMinuto` or `./eMinuto`

## Future Development

This prototype is intended to demonstrate that the concept works and how it can be utilized. 

However, a desktop application is not practical for many users. Therefore, the goal is to implement eMinuto for other platforms, especially mobile devices.
If you have expertise in such development or can support in other ways, please reach out to us.

## Contribute

You are very welcome to:
- download and test the prototype
- report bugs 
- create feature requests
- enhance the code
- star this repository
- promote eMinuto
- provide other support
- donate via [Liberapay](https://liberapay.com/freemind) or [PayPal](https://paypal.me/segalek)

## Contact

hello (at) eminuto (dot) org

## License

This project is licensed under the MIT License.