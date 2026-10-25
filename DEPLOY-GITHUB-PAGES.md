# GitHub Pages-এ ডিপ্লয় গাইড — `tezofy.github.io/advertisingandmore.com/`

এই প্যাকেজটি **project site** হিসেবে ডিপ্লয়ের জন্য প্রস্তুত: `index.html` রিপোর রুটে,
সব অ্যাসেট **রিলেটিভ পাথে** (`assets/...`, `./...`), কোনো root-absolute (`/...`)
পাথ নেই — তাই subpath `/advertisingandmore.com/`-এও সব ছবি/ফন্ট/স্ক্রিপ্ট ঠিক লোড হবে।

## ফাইল কাঠামো

```
advertisingandmore.com/        ← GitHub রিপো (নাম ঠিক এটাই রাখুন)
├── .nojekyll                  ← Jekyll প্রসেসিং বন্ধ রাখে (ফাইল হুবহু সার্ভ হয়)
├── index.html                 ← মূল ল্যান্ডিং পেজ
├── assets/                    ← 170টি WebP ও অন্যান্য অ্যাসেট (রিলেটিভ পাথ)
├── ai-icons/
├── build-fragments/
├── build_top15.py             ← সোর্স বিল্ডার (পেজ রিজেনারেট করতে লাগে)
├── capture_full.py
├── docs/                      ← AUDIT, HANDOFF
├── README.md
└── DEPLOY-GITHUB-PAGES.md     ← এই ফাইল
```

## ধাপ ১ — রিপো তৈরি (web UI)

1. GitHub-এ লগইন করে **New repository** → নাম দিন **`advertisingandmore.com`**
   (owner: `tezofy`) → Public → Create repository।
2. এই প্যাকেজের **সব ফাইল ও ফোল্ডার** রিপোর রুটে আপলোড করুন
   (web UI: **Add file → Upload files**; ফোল্ডারসহ টেনে ছাড়লেই হবে)।
   `.nojekyll` লুকানো ফাইল — টেনে ছাড়ার সময় অবশ্যই যেন আপলোড হয়।
3. **Commit changes**।

## ধাপ ২ — Pages চালু

1. রিপোর **Settings → Pages**-এ যান।
2. **Build and deployment → Source: “Deploy from a branch”**।
3. **Branch: `main`**, ফোল্ডার: **`/ (root)`** → Save।
4. ১–২ মিনিট পর সাইট লাইভ হবে:
   **https://tezofy.github.io/advertisingandmore.com/**

## ধাপ ১ (বিকল্প) — Git কমান্ড দিয়ে

```bash
# প্যাকেজ ফোল্ডারের ভেতরে
git init
git add .
git commit -m "Party Services & Rentals landing page"
git branch -M main
git remote add origin https://github.com/tezofy/advertisingandmore.com.git
git push -u origin main
# তারপর ধাপ ২ (Settings → Pages) অনুসরণ করুন
```

## পরে আপডেট করার নিয়ম

- কনটেন্ট বদলালে শুধু `index.html` (প্রয়োজনে `assets/`) নতুন করে commit/push দিন;
  Pages নিজে থেকে রিবিল্ড করবে।
- বড় পরিবর্তন `build_top15.py` দিয়ে রিজেনারেট করে তারপর `index.html` পুশ করুন —
  কখনোই শুধু জেনারেট করা HTML-এ হাতে প্যাঁচ মারবেন না।

## ডিপ্লয়-চেকলিস্ট

- [ ] রিপোর নাম `advertisingandmore.com`, ফাইলগুলো রুটে (ফোল্ডারের ভেতরে নয়)
- [ ] `.nojekyll` আপলোড হয়েছে
- [ ] https://tezofy.github.io/advertisingandmore.com/ খুললে হিরো ছবিসহ পেজ আসে
- [ ] DevTools Network-এ কোনো 404 নেই (বিশেষ করে `assets/img/*.webp`)
- [ ] “CLICK FOR COFFEE” ও “Request a Quote” `#contact`-এ নিয়ে যায়
- [ ] Careers লিঙ্ক লাইভ সাইটে (`advertisingandmore.com/job-vacancy-page.html`) যায়

## নোট

- হেডার/ফুটারের Home/About/Reviews ইত্যাদি লিঙ্ক ইচ্ছাকৃতভাবে লাইভ
  `advertisingandmore.com`-এর anchor-এ পয়েন্ট করে — এগুলো এই এক-পেজ সাইটের
  সেকশন নয়, তাই subpath-এ 404 হবে না।
- কোনো কাস্টম ডোমেইন যোগ না করলে URL থাকবে `tezofy.github.io/advertisingandmore.com/`;
  কাস্টম ডোমেইন লাগলে Settings → Pages → Custom domain-এ বসানো যাবে (CNAME ফাইল নিজে তৈরি হবে)।
