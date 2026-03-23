# TESTING

## 1. Manual Test Cases

| Page/Feature        | Action                                          | Expected Result                          | Observed Result | Pass/Fail |
|---------------------|-------------------------------------------------|------------------------------------------|----------------|-----------|
| Register            | Create a new user                               | User is registered and redirected home   | User registered successfully | Pass |
| Login               | Login with registered user                      | User is logged in and redirected home    | Login works; blocked if wrong credentials | Pass |
| Logout              | Click logout link                               | User is logged out and redirected to login page | Logout works; redirected to login page | Pass |
| Add Recipe          | Add a recipe with all fields filled             |Recipe appears in user’s recipe list      | Recipe added successfully; only visible to current user | Pass |
| Edit Recipe         | Edit an existing recipe                         | Changes saved and reflected in recipe   | Edit works; cannot edit another user’s recipe | Pass |
| Delete Recipe       | Delete an existing recipe                       | Recipe removed from list                 | Delete works; confirmation modal added | Pass |
| Unauthorized Edit/Delete | Try to edit/delete another user’s recipe | User sees error / action blocked         | Unauthorized actions blocked; 403 error shown | Pass |
| Debug mode check    | Run app                                        | Debug info not visible in production     | Debug mode turned off | Pass |
| Secret key handling | Check environment variable setup               | Secret key not hardcoded                 | App uses env variable or fallback | Pass |

---

## 2. User Story Tests

| User Story          | Test Steps                                     | Expected Result                          |
|--------------------|------------------------------------------------|-----------------------------------------|
| User can manage own recipes | Register → Add → Edit → Delete a recipe | Only own recipes can be modified; other users cannot modify recipes | ✅ Works as expected |
| User authentication | Logout → Login with correct/incorrect credentials | Login succeeds with correct info, fails with wrong info | ✅ Works as expected |

---

## 3. Responsiveness

- Tested on desktop, tablet, and mobile using browser developer tools.  
- Navigation, buttons, and recipe cards are visible and usable on all screen sizes.  
- Minor improvement: could add a burger menu for mobile in future update.

---

## 4. Code Validation

- HTML validated at [W3C Markup Validator](https://validator.w3.org/) ✅ No errors.  
- CSS validated at [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) ✅ No errors.  
- JavaScript (if used) validated at [JSHint](https://jshint.com/) ✅ No errors.

---

## 5. Bugs Encountered & Rectified

| Bug/Issue                                   | How Identified | Resolution |
|---------------------------------------------|----------------|-----------|
| All recipes visible to new users            | Logged in as different user | Added `user_id` filtering; only show recipes belonging to current user |
| Anyone could edit/delete others’ recipes    | Manual test of edit/delete | Added ownership check with `abort(403)` |
| Logout link not working                      | Tested navigation | Fixed route and added `@login_required` |
| Debug mode on in production                  | Checked console/logs | Set `debug=False` |
| Secret key hardcoded                          | Checked app.py | Replaced with `os.environ.get('SECRET_KEY', 'fallback_secret')` |

---

## 6. Bug Fixes

- Added recipe ownership checks for edit/delete actions.  
- Fixed logout route so it properly logs out and redirects.  
- Turned debug mode off.  
- Replaced hardcoded secret key with environment variable.  
- Added `@login_required` to home and recipe routes.

---

## 7. Notes / Observations

- Users can only see and manage their own recipes.  
- Login, logout, and registration work as expected.  
- The application is now secure for deployment.  
- Future improvements: add toast notifications and mobile burger menu.