
<!DOCTYPE html>
<html lang="en" data-color-mode="auto" data-light-theme="light" data-dark-theme="dark"  data-a11y-animated-images="system" data-a11y-link-underlines="false">


  <head>
    <meta charset="utf-8">

  <title>Initiating SAML single sign-on</title>
  <meta http-equiv="refresh" content="0;url=https://login.w3.ibm.com/saml/sps/saml20ip/saml20/login?RelayState=2FxxvEP4s2CbY3L7-1j522KPli78bJNx57tslxDc1v1m80wHVxH77jz4lst1ZJ7z3QWff1fhsyDV8hgB8uu9mbNBCUmWtSJuKmwBYYd7-T8&amp;SAMLRequest=fZJdb9sgFIbv%2Byss7uPvjATFqdxG1SJ1jdVku9hNheE4QbLB4%2BB0%2B%2FclTqp16to7BM%2BB9zmHxfXvrg2OYFEZXZAkjMn18mqBvGt7Vg7uoB%2Fh1wDoAs9pZONBQQarmeGokGneATIn2Lb8ds%2FSMGa9Nc4I05I3JZ9XcESwzgcgwXpVkCcqY0hoLDhPp0LOqOQAX%2FI8SWROc9rIhPI5pWI%2Br7NZmtVyOgU5i6HOGyry2Zz6axAHWGt0XLuCpHGaT5J4kma7ZM6ylCXpTxL8eJX2EUiw8o5KczfuHJzrkUVRa%2FZKh89ZqOouFKaLTi4R9jgu0lj1l8WZPL1beRl1hII0vEUgQXXpxo3SUun9542ozxCyr7tdNak22x0Jytfm3BqNQwd2C%2FaoBHx%2FvP8bdK%2FcYaj%2FjSnOPFmO02RjS%2Bzy%2FxWL6C1zGf%2BDz7deVaZV4k9Qtq15vrXAnXdzdvBqd8Z23H1slITJuKPkpBlRNmjsQahGgSTRJZfXkurkh8GDcTfgUfhoZB7Y6I0tGwf2HUNHxl8bvf%2B9y6sX&amp;SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&amp;Signature=VQGPRNi0eoky8uFM6%2B9mAsWpnKvhBOCuJrZwBoRvVBE32a5YlBG275FthnY1mEmQdZsW68c3YJRCRN%2FyExgl9S%2FiGZ%2FflFiL9Mnpe8LuEPVhm%2BBTrWFlUSM%2FzUUHt0iIOQS%2BRMN6YseUnIbL%2FpTYLNsC%2FO12N4Q2QohMPACDSaFswcYBts6Meerc7okr%2FabFxfE0dznbNZSATYevqKqY1a6qwmsK4rtuiwgpnGZ3ozlY%2Fkd0lKSXR5lUalzfLuVhhLl3v24PagZWQWzk6GaO7YiyUxcEwAQaBTW3TRdIixlM%2BPLwOFvm6yHH9wYkYRRNMnTJXFtH69deAtSAPyDWimnzCyOaZ5CPVSQ9rQ7Tf55RJzuGgqTgyItEx8ZSkt0Sv0LJwKUYAPomWXy7VIS621nCxYVpg2lkIQY32oXUR4JiKduAbdiqvLpD16MKiimrtk5SG7UNCLdZpgTfJYkdIH%2Fb1Y5up31Sdv8bbG81COqDrjup7uIw4hFbdlcE5JJh87g4DTbgiJ5RfyyVBPHKLYwmApst5HhriLv1yKa5z7gQ9Hv1%2Be4VlagBuP0DL%2BwoCF4EI2KqiWiu5SN3TU2FhhsIZc16RK9LrG39zETFoZ9C3v6Yu97eokpHyB9%2BXgDtDKlgpQshuzazUBKAS6bJvahn9m8XLRDuK6RJEYerG5Y%3D" data-url="https://login.w3.ibm.com/saml/sps/saml20ip/saml20/login?RelayState=2FxxvEP4s2CbY3L7-1j522KPli78bJNx57tslxDc1v1m80wHVxH77jz4lst1ZJ7z3QWff1fhsyDV8hgB8uu9mbNBCUmWtSJuKmwBYYd7-T8&amp;SAMLRequest=fZJdb9sgFIbv%2Byss7uPvjATFqdxG1SJ1jdVku9hNheE4QbLB4%2BB0%2B%2FclTqp16to7BM%2BB9zmHxfXvrg2OYFEZXZAkjMn18mqBvGt7Vg7uoB%2Fh1wDoAs9pZONBQQarmeGokGneATIn2Lb8ds%2FSMGa9Nc4I05I3JZ9XcESwzgcgwXpVkCcqY0hoLDhPp0LOqOQAX%2FI8SWROc9rIhPI5pWI%2Br7NZmtVyOgU5i6HOGyry2Zz6axAHWGt0XLuCpHGaT5J4kma7ZM6ylCXpTxL8eJX2EUiw8o5KczfuHJzrkUVRa%2FZKh89ZqOouFKaLTi4R9jgu0lj1l8WZPL1beRl1hII0vEUgQXXpxo3SUun9542ozxCyr7tdNak22x0Jytfm3BqNQwd2C%2FaoBHx%2FvP8bdK%2FcYaj%2FjSnOPFmO02RjS%2Bzy%2FxWL6C1zGf%2BDz7deVaZV4k9Qtq15vrXAnXdzdvBqd8Z23H1slITJuKPkpBlRNmjsQahGgSTRJZfXkurkh8GDcTfgUfhoZB7Y6I0tGwf2HUNHxl8bvf%2B9y6sX&amp;SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&amp;Signature=VQGPRNi0eoky8uFM6%2B9mAsWpnKvhBOCuJrZwBoRvVBE32a5YlBG275FthnY1mEmQdZsW68c3YJRCRN%2FyExgl9S%2FiGZ%2FflFiL9Mnpe8LuEPVhm%2BBTrWFlUSM%2FzUUHt0iIOQS%2BRMN6YseUnIbL%2FpTYLNsC%2FO12N4Q2QohMPACDSaFswcYBts6Meerc7okr%2FabFxfE0dznbNZSATYevqKqY1a6qwmsK4rtuiwgpnGZ3ozlY%2Fkd0lKSXR5lUalzfLuVhhLl3v24PagZWQWzk6GaO7YiyUxcEwAQaBTW3TRdIixlM%2BPLwOFvm6yHH9wYkYRRNMnTJXFtH69deAtSAPyDWimnzCyOaZ5CPVSQ9rQ7Tf55RJzuGgqTgyItEx8ZSkt0Sv0LJwKUYAPomWXy7VIS621nCxYVpg2lkIQY32oXUR4JiKduAbdiqvLpD16MKiimrtk5SG7UNCLdZpgTfJYkdIH%2Fb1Y5up31Sdv8bbG81COqDrjup7uIw4hFbdlcE5JJh87g4DTbgiJ5RfyyVBPHKLYwmApst5HhriLv1yKa5z7gQ9Hv1%2Be4VlagBuP0DL%2BwoCF4EI2KqiWiu5SN3TU2FhhsIZc16RK9LrG39zETFoZ9C3v6Yu97eokpHyB9%2BXgDtDKlgpQshuzazUBKAS6bJvahn9m8XLRDuK6RJEYerG5Y%3D">
  <meta name="viewport" content="width=device-width">
  <link crossorigin="use-credentials" media="all" rel="stylesheet" href="https://assets.github.ibm.com/assets/light-a09cef873428.css" /><link crossorigin="use-credentials" media="all" rel="stylesheet" href="https://assets.github.ibm.com/assets/dark-5d486a4ede8e.css" /><link data-color-theme="dark_dimmed" crossorigin="use-credentials" media="all" rel="stylesheet" data-href="https://assets.github.ibm.com/assets/dark_dimmed-27c8d635e4e5.css" /><link data-color-theme="dark_high_contrast" crossorigin="use-credentials" media="all" rel="stylesheet" data-href="https://assets.github.ibm.com/assets/dark_high_contrast-8438e75afd36.css" /><link data-color-theme="dark_colorblind" crossorigin="use-credentials" media="all" rel="stylesheet" data-href="https://assets.github.ibm.com/assets/dark_colorblind-bf5665b96628.css" /><link data-color-theme="light_colorblind" crossorigin="use-credentials" media="all" rel="stylesheet" data-href="https://assets.github.ibm.com/assets/light_colorblind-c414b5ba1dce.css" /><link data-color-theme="light_high_contrast" crossorigin="use-credentials" media="all" rel="stylesheet" data-href="https://assets.github.ibm.com/assets/light_high_contrast-e5868b7374db.css" /><link data-color-theme="light_tritanopia" crossorigin="use-credentials" media="all" rel="stylesheet" data-href="https://assets.github.ibm.com/assets/light_tritanopia-299ac9c64ec0.css" /><link data-color-theme="dark_tritanopia" crossorigin="use-credentials" media="all" rel="stylesheet" data-href="https://assets.github.ibm.com/assets/dark_tritanopia-3a26e78ad0ff.css" />
  <link crossorigin="use-credentials" media="all" rel="stylesheet" href="https://assets.github.ibm.com/assets/primer-047ee6293fcd.css" />
  <link crossorigin="use-credentials" media="all" rel="stylesheet" href="https://assets.github.ibm.com/assets/global-7f2d4e2ce2fe.css" />



  <link rel="mask-icon" href="https://assets.github.ibm.com/pinned-octocat.svg" color="#000000">
  <link rel="alternate icon" class="js-site-favicon" type="image/png" href="https://assets.github.ibm.com/favicons/favicon-ent.png">
  <link rel="icon" class="js-site-favicon" type="image/svg+xml" href="https://assets.github.ibm.com/favicons/favicon-ent.svg">

<meta name="theme-color" content="#1e2327">
<meta name="color-scheme" content="light dark" />


  <link rel="manifest" href="/manifest.json" crossOrigin="use-credentials">

  </head>

  <body  style="word-wrap: break-word;">
    <div data-turbo-body  style="word-wrap: break-word;">


<div class="container-md px-3">
  <div data-view-component="true" class="blankslate mt-5">
    <svg aria-hidden="true" height="24" viewBox="0 0 24 24" version="1.1" width="24" data-view-component="true" class="octicon octicon-shield-lock blankslate-icon">
    <path d="M11.46 1.137a1.748 1.748 0 0 1 1.08 0l8.25 2.675A1.75 1.75 0 0 1 22 5.476V10.5c0 6.19-3.77 10.705-9.401 12.83a1.704 1.704 0 0 1-1.198 0C5.771 21.204 2 16.69 2 10.5V5.476c0-.76.49-1.43 1.21-1.664Zm.617 1.426a.253.253 0 0 0-.154 0L3.673 5.24a.25.25 0 0 0-.173.237V10.5c0 5.461 3.28 9.483 8.43 11.426a.199.199 0 0 0 .14 0c5.15-1.943 8.43-5.965 8.43-11.426V5.476a.25.25 0 0 0-.173-.237ZM13 12.232V15a1 1 0 0 1-2 0v-2.768a2 2 0 1 1 2 0Z"></path>
</svg>
    <h3 data-view-component="true" class="mb-1">You are being redirected to your identity provider in order to authenticate.</h3>

    <p>
      If your browser does not redirect you back, please <a id="redirect" aria-label="click here to redirect you back" class="Link--inTextBlock" href="https://login.w3.ibm.com/saml/sps/saml20ip/saml20/login?RelayState=2FxxvEP4s2CbY3L7-1j522KPli78bJNx57tslxDc1v1m80wHVxH77jz4lst1ZJ7z3QWff1fhsyDV8hgB8uu9mbNBCUmWtSJuKmwBYYd7-T8&amp;SAMLRequest=fZJdb9sgFIbv%2Byss7uPvjATFqdxG1SJ1jdVku9hNheE4QbLB4%2BB0%2B%2FclTqp16to7BM%2BB9zmHxfXvrg2OYFEZXZAkjMn18mqBvGt7Vg7uoB%2Fh1wDoAs9pZONBQQarmeGokGneATIn2Lb8ds%2FSMGa9Nc4I05I3JZ9XcESwzgcgwXpVkCcqY0hoLDhPp0LOqOQAX%2FI8SWROc9rIhPI5pWI%2Br7NZmtVyOgU5i6HOGyry2Zz6axAHWGt0XLuCpHGaT5J4kma7ZM6ylCXpTxL8eJX2EUiw8o5KczfuHJzrkUVRa%2FZKh89ZqOouFKaLTi4R9jgu0lj1l8WZPL1beRl1hII0vEUgQXXpxo3SUun9542ozxCyr7tdNak22x0Jytfm3BqNQwd2C%2FaoBHx%2FvP8bdK%2FcYaj%2FjSnOPFmO02RjS%2Bzy%2FxWL6C1zGf%2BDz7deVaZV4k9Qtq15vrXAnXdzdvBqd8Z23H1slITJuKPkpBlRNmjsQahGgSTRJZfXkurkh8GDcTfgUfhoZB7Y6I0tGwf2HUNHxl8bvf%2B9y6sX&amp;SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&amp;Signature=VQGPRNi0eoky8uFM6%2B9mAsWpnKvhBOCuJrZwBoRvVBE32a5YlBG275FthnY1mEmQdZsW68c3YJRCRN%2FyExgl9S%2FiGZ%2FflFiL9Mnpe8LuEPVhm%2BBTrWFlUSM%2FzUUHt0iIOQS%2BRMN6YseUnIbL%2FpTYLNsC%2FO12N4Q2QohMPACDSaFswcYBts6Meerc7okr%2FabFxfE0dznbNZSATYevqKqY1a6qwmsK4rtuiwgpnGZ3ozlY%2Fkd0lKSXR5lUalzfLuVhhLl3v24PagZWQWzk6GaO7YiyUxcEwAQaBTW3TRdIixlM%2BPLwOFvm6yHH9wYkYRRNMnTJXFtH69deAtSAPyDWimnzCyOaZ5CPVSQ9rQ7Tf55RJzuGgqTgyItEx8ZSkt0Sv0LJwKUYAPomWXy7VIS621nCxYVpg2lkIQY32oXUR4JiKduAbdiqvLpD16MKiimrtk5SG7UNCLdZpgTfJYkdIH%2Fb1Y5up31Sdv8bbG81COqDrjup7uIw4hFbdlcE5JJh87g4DTbgiJ5RfyyVBPHKLYwmApst5HhriLv1yKa5z7gQ9Hv1%2Be4VlagBuP0DL%2BwoCF4EI2KqiWiu5SN3TU2FhhsIZc16RK9LrG39zETFoZ9C3v6Yu97eokpHyB9%2BXgDtDKlgpQshuzazUBKAS6bJvahn9m8XLRDuK6RJEYerG5Y%3D">click here</a> to continue.
    </p>

</div></div>


    </div>

    <div id="js-global-screen-reader-notice" class="sr-only" aria-live="polite" ></div>
  </body>
</html>
