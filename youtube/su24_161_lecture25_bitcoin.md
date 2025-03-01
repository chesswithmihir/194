# CS 161 Su24, Lecture 25 - Bitcoin
## Taught my Peyrin Kao

## Today: Bitcoin

- Bitcoin: sending and receiving money without trusting a central authority
- how does it work?
	- How do we manage identity, transactions, and balances on the ledger?
	- How do we construct a decentralized, trusted ledger?
- The trouble with Bitcoin
- Bitcoin in practice

## Problem Statement: The Decentralized Bank

- Alice, Bob, Carole and Dave each have money
- Anyone can send money to anyone else
- bank remembers everyones balances and updates with transactions
- you cannot spend more money than you have
- no party trusts any other party and there is no central authority in bitcoin
	- rely on cryptography to not trust a bank or any central authority

## Identity Management

- if you want to send money to Alice, how do you identify who Alice is?
- one protocol to id someone is probably a certificate with a ds sign key and a public key
- but we said with our banks we can't trust anybody and that includes central authorities or root CAs which we don't want
- Can't have Alice's public key signed by someone you can trust because there isn't anyone you can trust when designing bitcoin
- We are going to cheat a lil and so if you want to send money to someone, you have to know what their public key is and bitcoin does not map public keys to people in anyway
- when we talk about users in bitcoin, we meet someone with public key A, B, C, D. We don't care about these people or their identities, we only need to know their public keys.

## Transactions

- To keep track of what money has been spent, use a public ledger
- bulletin board accessible to everyone, append-only
- immutable: nobody can change or delete existing data
- this is a central authority for now, but we'll deal with it later.
- How do we record transactions in a way that everyone can see them?
- Idea: Put PKd paid PKa 10 coins on the ledger
- Problem! No crypto! Mallory can come say PKa should PKm 10,000 coins!
- Mallory has spent someone elses money by adding to the ledger.
- Use Digital Signatures!!! Make sure people who are adding to the lecture are signing with their own key!
- How do we verify that there are enough coins tho? Look at the ledger!
- All of the transactions that have ever been made at any time exists on the ledger. It doesn't tell me how much money someone has. If you look at it, there are only transactions not balances.
- To compute it, you would have to look through the history of all transactions in history to figure out how many coins someone has. This can be very slow as the ledger goes big.
- How can we do better? Instead of scanning through the ledger to figure out how much money someone has, we can instead force every transaction to cite its sources and tell us if you want to spend 10 coins, where are those 10 coins coming out of, citing your sources
- more formally every transaction has an input citing where you have the coins and who you are sending it to.
- now all you have to do is to state that you are going to use money from transaction 2 and transaction 4 to pay for this new transaction to PKa and PKb and here is my digital signature.
- 
