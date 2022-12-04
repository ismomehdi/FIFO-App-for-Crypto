# FIFO App for Crypto (*Work in Progress...*)

Lue sovelluksen kuvaus [täältä](https://github.com/ismomehdi/FIFO-App-for-Crypto/blob/main/about.md).

## Välipalautus 3

Sovelluksella on pääpiirteissään toimiva pohja, jonka avulla tietokantaan voi lisätä ostoja ja myyntejä. Sovellus laskee tietokantaan lisättyjen myyntien tuotot ja tappiot FIFO-periaatteen mukaisesti SQL:ssä. Sovellukseen voi rekisteröityä ja kirjautua sisään. Sivuilla voi myös jättää palautetta.

Virheiden käsittely puuttuu vielä. Tuotannossa olevassa sovelluksessa vaikuttaisi olevan bugi, jonka vuoksi History-sivu ei ensimmäisellä latauskerralla toimi. Sen jälkeen bugi ei kuitenkaan vaikuta toistuvan.

Tehtävää on virheiden käsittelyn lisäksi myös koodin refaktoroinnissa ja jakamisessa moduuleihin sekä SQL-komentojen yksinkertaistamisessa. CSRF-haavoittuvuus täytyy vielä korjata.

Sovellus löytyy [täältä](https://tsoha-fifo-app.fly.dev/).

