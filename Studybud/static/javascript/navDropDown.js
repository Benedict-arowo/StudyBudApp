const dropDownIcon = document.getElementById('dropdown')
const dropDownMenu = document.getElementById('dropDownMenu')
const settings = document.getElementById('settings')
const logout = document.getElementById('logout')

dropDownIcon.addEventListener('click', e => {
    dropDownMenu.classList.toggle('active')
})

settings.onclick = () => {
    open('/settings', '_self')
}


logout.onclick = () => {
    open('/logout', '_self')
}

