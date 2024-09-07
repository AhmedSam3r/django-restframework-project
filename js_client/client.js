const loginForm = document.getElementById('login-form')
const searchForm = document.getElementById('search-form')

const contentContainer = document.getElementById('content-container')
const baseEndpoint = "http://localhost:8000/api"


if (loginForm){
    // handle form's data
    loginForm.addEventListener('submit', handleLogin)
}

if (searchForm){
    // handle form's data
    searchForm.addEventListener('submit', handleSearch)
}


function handleSearch(event){
    console.log(event);
    // prevents event from submitting
    event.preventDefault()
    let searchFormData = new FormData(searchForm)
    let searchObjectData = Object.fromEntries(searchFormData)

    let searchParams = new URLSearchParams(searchObjectData)
    const searchEndpoint = `${baseEndpoint}/search/?public=true&${searchParams}`

    console.log('searchObjectData = ',searchObjectData)
    const options = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer lol"

        },x
    }
    console.log('searchEndpoint ',searchEndpoint);
    console.log('options', options);

    fetch(searchEndpoint, options).
    then(response => {
        console.log(response);
        return response.json()
    }).then(data => {
        writeToContainer(data)
    }).catch(err=> {
        console.log('err', err);
    })

}





function writeToContainer(data){
    if(contentContainer){
        // create new html with the data we're  passing in this container element
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data) + "</pre>"
        
    }
}

function validateJWTToken(){
    const endpoint = `${baseEndpoint}/token/verify/`
    const access_tok = String(localStorage.getItem('access'))
    console.log('access_tok = ', );
    const options = getFetchOption("POST", {"token": access_tok})
    console.log("validateJWTToken():OPTIONS ", options);
    fetch(endpoint, options)
    .then(response => {
      if (!response.ok) {
        console.log(`HTTP error! Status: ${response.status}`);
      }
    //   return response.json();
    })
    .then(data => {
        console.log('data is ', data)
        if (data){
            const tokenValid = TokenNotValid(data);
            // if valid okay
            if (tokenValid){
              alert('Token is validate, good job')
            }      
        }
        else{
            access_token = refreshJWTToken()
            localStorage.setItem("access", String(access_token))
            console.log("validateJWTToken after refreshing= ", access_token);
            return  access_token
        }
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle the error here, e.g., show an error message to the user.
    });
}

function refreshJWTToken(){
    const endpoint = `${baseEndpoint}/token/refresh/`
    const options = getFetchOption("POST", {"refresh": localStorage.getItem('refresh')})
    console.log("refreshJWTToken ", options);
    fetch(endpoint, options)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
        // writing the new token
        localStorage.setItem("access", data)
        console.log('after refresh data', data);
        writeToContainer(data)
        return data.access
        // if valid okay
        // else make a login to refresh the token using refresh api
    })
    .catch(error => {
      console.error('Error:', error);
      // Handle the error here, e.g., show an error message to the user.
    });
}


function getFetchOption(method, body){
    return {
        method: method === null? "GET": method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('access')}`,
            // "HTTP_AUTHORIZATION": `Bearer ${localStorage.getItem('access')}`,
        },
        body: body ? JSON.stringify(body) : null
    }
}


function getProductList(){
    const endpoint = `http://localhost:8000/product/list-or-create/`
    console.log('----product listlocalStorage----', {"token": localStorage.getItem('access')});
    const options = getFetchOption("GET")
    console.log('calling product', endpoint, options);
    fetch(endpoint, options)
    .then(response =>response.json())
    .then(response=>{
        console.log(response);
        const validToken = TokenNotValid(response)
        if (validToken){
            writeToContainer(response);
        }
        console.log('No writing');
        return response.json()
    }).catch(err=>{
        console.log('product error', err);

    })
}

function handleAuthData(authData, callback){
    localStorage.setItem('access', authData.access)
    localStorage.setItem('refresh', authData.refresh)
    console.log('callback', authData.access, authData.refresh);
    console.log('@@@ localStorage.getItem @@@@',localStorage.getItem('access'))

    if (callback){
        console.log('inside calling callback');
        callback()
    }
}

function handleLogin(event){
    console.log(event);
    // prevents event from submitting
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    // get the formdata from the login form element then convert it into an object
    let loginFormData = new FormData(loginForm)
    let loginObjectData = Object.fromEntries(loginFormData)
    console.log(loginObjectData["username"])
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(loginObjectData)
    }
    console.log('options', options);
    console.log('loginEndpoint ',loginEndpoint);
    fetch(loginEndpoint, options).
    then(response => {
        console.log(response);
        return response.json()
    }).then(authData => {
        handleAuthData(authData, getProductList)
    }).catch(err=> {
        console.log('err', err);
    })

}

function TokenNotValid(jsonData){
    if (jsonData.code && jsonData.code === 'token_not_valid'){
        alert("Token expired, please login")
        return false;
    }
    return true
}

validateJWTToken()
// getProductList()