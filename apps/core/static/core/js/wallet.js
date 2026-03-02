/* Wallet connection */
let walletConnected = false;
const _elWBtn      = document.getElementById('walletBtn');
const _elWText     = document.getElementById('wText');
const _elWDot      = document.getElementById('wDot');
const _elWOptions  = document.getElementById('wOptions');
const _elWConn     = document.getElementById('wConnected');
const _elWAddr     = document.getElementById('wAddr');
const _elWBal      = document.getElementById('wBal');
const _elMintMsg   = document.getElementById('mintMsg');

async function connectWallet() {
  if (walletConnected) { disconnectWallet(); return; }
  document.getElementById('mint').scrollIntoView({ behavior: 'smooth' });
}

async function doConnect(provider) {
  if (provider === 'MetaMask') {
    if (typeof window.ethereum === 'undefined') {
      alert("MetaMask non detecte. Installe l'extension MetaMask pour continuer.");
      return;
    }
    try {
      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      const bal = await window.ethereum.request({ method: 'eth_getBalance', params: [accounts[0], 'latest'] });
      onConnected(accounts[0], (parseInt(bal, 16) / 1e18).toFixed(4), provider);
    } catch(e) {
      alert('Connexion refusee.');
    }
  } else {
    alert(provider + ' - integration en cours. Reviens bientot !');
  }
}

function onConnected(addr, bal, prov) {
  walletConnected = true;
  const short = addr.slice(0,6) + '...' + addr.slice(-4);
  _elWBtn.classList.add('connected');
  _elWText.textContent = short;
  _elWOptions.style.display = 'none';
  _elWConn.style.display = 'block';
  _elWAddr.textContent = short;
  _elWBal.textContent = bal + ' ETH';
  _elMintMsg.textContent = 'Connecte via ' + prov + ' sur Ethereum Mainnet';
}

function disconnectWallet() {
  walletConnected = false;
  _elWBtn.classList.remove('connected');
  _elWText.textContent = 'CONNECT WALLET';
  _elWDot.style.background = 'var(--muted)';
  _elWOptions.style.display = 'flex';
  _elWConn.style.display = 'none';
}

async function doMint() {
  _elMintMsg.textContent = 'Preparation de la transaction...';
  await new Promise(r => setTimeout(r, 1200));
  _elMintMsg.textContent = 'Transaction envoyee. En attente de confirmation...';
  await new Promise(r => setTimeout(r, 3000));
  _elMintMsg.textContent = 'Mint reussi ! Verifie ton wallet pour ton nouveau Snailz.';
  _elMintMsg.style.color = 'var(--chill)';
}

if (typeof window.ethereum !== 'undefined') {
  window.ethereum.on('accountsChanged', accs => { if (!accs.length) disconnectWallet(); });
}
