# LockNKey
## Improving Cloud Security Systems using Threshold Cryptography

#### While data is being uploaded to cloud storage, it is vulnerable to attacks. It can be tampered with or stolen. Thus before uploading, we’ll be securing the data with the concept of threshold cryptography using the RSA algorithm. The processes such as Shamir’s Secret Sharing and Lagrange Interpolation Method have been used to further increase and improve the security of the data being stored. In this approach, there is no need for a user certification mechanism between user and Distributed Data Centers. Other approaches assume that there is a certification mechanism which in case if isn't present then there exists a threat that encryption key may be leaked by the malicious user who acquired the hardware wallet(storing the keys) lost by the user, since it is possible to collect at least t number of optional key fragments.

#### The user will be required to set up their Google Drive credentials to login into their account. Then the user can select whether they want to encrypt and upload or download and decrypt. If the user chooses to encrypt, the user’s data will be encrypted using a modified RSA algorithm which uses Proth and Mersenne prime numbers for additional security. The private key generated is then  split up into smaller parts or shares which can be stored at different places. The user must store these shares safely to decrypt the files.  When the user wants to decrypt the data he will require the minimum number of keys i.e. k out of the N total shares and then they can be used to recreate the private key using the Lagrange interpolation algorithm which allows us to reconstruct any polynomial of degree K-1 from K points on its curve. Thus the system is even more protected since an attacker will not be able to decode the data even if he has as many as k-1 shares.

#### The approach we have used allows the Implementation to be a GUI based application that can be used to improve the security of files stored on the cloud by using a process of encryption. The current verison uses Google Drive for cloud support.

## Flow chart 
<h2> Encrypt </h2>
<p align="center">
    <img src="img/encrypt.png" >
</p>
<h2> Decrypt </h2>
<p align="center">
  <img  src="img/decrypt.png">
</p>


<h2>Comparison Study of Propopsed Algorithm </h2>

<p align="center">
  <img  src="img/table.png">
</p>

<p align="center">
  <img  src="img/encrypt_graph.png">
</p>

<p align="center">
  <img  src="img/decrypt_graph.png">
</p>


## Contributors

<a href="https://github.com/avats101/LockNKey/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=avats101/LockNKey" />
</a>


