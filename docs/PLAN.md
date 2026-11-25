# Barber site plan

## Goal
A website for my barber business: clients book online, I manage bookings as admin.

## Decisions
- No client accounts: the booking form asks for name, email, phone, date and time
- Working hours: 10:00-20:00
- Services: haircut (30 min), haircut and beard (45 min)
- Languages: Uzbek, Russian, English

## Steps
1. Slots API (free times per date)
2. Public pages: home and booking form
3. Admin: login, bookings table, search, edit, delete
4. Design and UX
5. PostgreSQL and .env
6. Deploy: hosting, domain, HTTPS
7. Google: Search Console, sitemap, Google Business Profile
8. Extras: Telegram notification, cancel link