# Introduction

elm is a web-based licensing system with a simple, full-featured 
JSON API for making license enforcement requests. This package
is a client API for integrating into your python applications
in order to license through elm. This package is based on python
version 3.7.

The elm client API for python provides implementations of the elm 
web API for python-based applications. The API is designed around
a single abstraction, called a control manager, that simplifies 
the steps needed to add licensing to a client application. 

The control manager implementation provided in this package is
only suitable for desktop programs. It offers functions to:
- Register an instance and user of a product
- Validate that the current instance and user have access to the
  product
- Manage client-side state, such as registration status and
  instance and user UUIDs
- Support grace periods that allow users to access the product
  while offline
- Detect whether the end-user is modifying the system clock in
  order to gain unauthorized access to the product
  
It is up to the ISV to ensure that the state object produced
by the control manager is stored using a secure storage method,
i.e., stored in an encrypted manner on the end-user's computer.
If the end-user is able to manipulate this state, then they can
bypass the licensing controls and gain unauthorized access.

For more information on how to use this client API, visit
[the documentation page](https://evoleap.github.io/elmdocs).  

# Changelog
## 1.1.1 - May 29, 2024
### Fixes
- Fixed error when registration fails
## 1.1.0 - Sep 24, 2020
### Added
- Support for consumable tokens in component checkout
## 1.0.1 - Sep 14, 2020
### Added
- Component checkout code in desktop sample
### Fixes
- Fixed component checkout code
- Turned on SSL verify to avoid warnings

