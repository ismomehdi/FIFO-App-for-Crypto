# FIFO App for Crypto (*Work in Progress...*)

This app calculates cryptocurrency profits and losses. It is designed for Finnish audience.

## Crypto Tax in Finland

Income received from trading cryptocurrencies is taxable and one is required to file any income and expenses. Sometimes this might get tricky as the cost of an asset is determined by using the FIFO principle.

### What's FIFO?

FIFO – *First In, First Out* – is an asset management principle in which assets bought first are sold first.

### So What's Tricky About It?

Well, imagine calculating costs of cryptocurrencies on hundreds or even thousands of trades. Trying to keep track of which piece of Bitcoin you bought first is difficult and tedious.

### Deemed Acquisition Cost

When calculating expenses for the tax report, you can use the *deemed acquisition cost* as an alternative to the real cost of an asset. The deemed acquisition cost of an asset is 20% of the selling price or 40% if you've owned the asset for over 10 years. Using the deemed acquisition cost could make sense if the real cost of an asset is less than the deemed one (as greater cost means less taxes).

## Crypto Tax Apps

* There's many crypto tax applications online which rely on automatically fetching and processing transaction data. However, often there's a lot of mistakes in the processed data and users have to manually go through everything to check for whatever happens to be wrong. **FIFO App for Crypto** doesn't automatically fetch data. 
* There's a [FIFO calculator](https://www.vero.fi/tietoa-verohallinnosta/yhteystiedot-ja-asiointi/verohallinnon_laskuri/fifo-laskuri/) in Tax Administration’s website. It's not very useful; it only supports one cryptocurrency at a time and therefore using it would be awkward for anyone with more than one asset in their portfolio.

## About the App (App Goals)

* An easy and simple tool for keeping record of crypto trades and estimating taxable income.
* Profit and loss calculated using the FIFO principle. Automatic use of the deemed acquisition cost when more beneficial.
* Sign in to access your data.
* Support for multiple assets.

## App Development Strategy

* UI based on ReactJS will be developed later on.
