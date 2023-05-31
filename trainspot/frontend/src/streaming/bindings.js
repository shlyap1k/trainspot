function subscription_succeeded (members, _this)  {
  //set the member count
  _this.usersOnline = members.count;
  _this.id = _this.channel.members.me.id;
  // document.getElementById("myid").innerHTML = ` My id is : ` + _this.id;
  members.each(member => {
    if (member.id != _this.channel.members.me.id) {
      _this.users.push(member.id);
    }
  });
}

function member_removed(member, _this) {
  var index = _this.users.indexOf(member.id);
  _this.users.splice(index, 1);
  if (member.id == _this.user.id) {
    _this.endCall();
  }
}


export default subscription_succeeded
