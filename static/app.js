function deleteUser(userId) {
    axios.delete(`http://127.0.0.1:5000/users/${userId}/delete`)
}