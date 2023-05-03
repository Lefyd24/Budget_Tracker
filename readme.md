

### Το παρόν project αποτελεί ένα απλό Budget Tracker δημιουργημένο σε Python Flask.

Το project έχει 4 διαφορετικά παρακλάδια:

* Παράθεση καθημερινών εξόδων και σύγκριση με budget από Flask Forms
* Διασύνδεση με βάση δεδομένων MongoDB με 3 collections - budget, balance & daily_expenses
* Σύστημα ειδοποίησης στο κινητό από το API του [Pushover](https://pushover.net/)
* Ασύγχρονη ειδοποίηση του κινητού μέσω δημιουργίας Job στο [Cron](https://www.easycron.com/user)



Before any update:

`<code>`pip freeze > requirements.txt `</code>`

For updates on the app run:

1) git add .
2) git commit -m "Description of the commit"
3) vercel
4) (if you want to create an alias for the latest deployment, you can run: vercel --prod)
