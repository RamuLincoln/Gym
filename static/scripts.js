function isOver18(dateOfBirth) {
    // find the date 18 years ago
    const date18YrsAgo = new Date();
    date18YrsAgo.setFullYear(date18YrsAgo.getFullYear() - 18);
    // check if the date of birth is before that date
    return dateOfBirth <= date18YrsAgo;
  }

  function onRegisterSubmit(msg)
  {
    var dateOfBirth = document.forms.AddMember.birthday.value;
    var over18 = isOver18(new Date(dateOfBirth));
    if(!over18)
    {
      alert("Member age must be over 18.");
      return false;
    }
    if(msg == 'add')
      alert("Member Added successfully!")
    else
    alert("Member registered successfully!")
    return true;
  }