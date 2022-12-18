# FIFO App for Crypto (*Work in Progress...*)

Lue sovelluksen kuvaus [täältä](documentation/about.md).

## Lopullinen palautus

Sovellukseen voi luoda tunnuksen ja kirjautua sisään. Sisäänkirjautunut käyttäjä voi lisätä sovellukseen ostoja sekä myyntejä ja tarkastella transaktiohistoriaansa. Sovellus lisää transaktiot tietokantaan ja laskee realisoidut tuotot ja tappiot [FIFO-periaatteen](https://www.investopedia.com/terms/f/fifo.asp) mukaisesti tuotekohtaisesti. Käyttäjä voi jättää palautetta Feedback-sivulla.

Sovellus löytyy [täältä](https://tsoha-fifo-app.fly.dev/).

### Tulevia kehityskohteita

- Mahdollisuus muokata ja poistaa lisättyjä transaktioita.
- Toiminto, joka estää myynnin lisäämisen, mikäli myyntiä edeltäviä ostoja ei ole tarpeeksi.
- Mahdollisuus lisätä useampi portfolio ja määrittää vakioportfolio (tietokannassa on jo taulut valmiina).
- FIFO-laskennasta vastaavan SQL-komennon optimointi.
- Käyttöliittymän suunnittelu ReactJS:lla.

