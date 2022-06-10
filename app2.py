import streamlit as st
from src.blockchain_utils.credentials import get_client
from src.services.nft_service import NFTService
from src.services.nft_marketplace import NFTMarketplace
from src.repository.nft_repository import NFTRepository
from src.repository.marketplace_repository import NFTMarketplaceRepository
import time
import algosdk

client = get_client()

if "admin" not in st.session_state:
    st.session_state.admin = algosdk.account.generate_account()
    st.session_state.NFT_owner = st.session_state.admin


if "buyer_1" not in st.session_state:
    st.session_state.buyer_1 = algosdk.account.generate_account()

if "app_is_deployed" not in st.session_state:
    st.session_state.app_is_deployed = False

if "NFT_image" not in st.session_state:
    st.session_state.NFT_image = None


if "transactions" not in st.session_state:
    st.session_state.transactions = []

admin_pk, admin_address = st.session_state.admin
buyer_1_pk, buyer_1_address = st.session_state.buyer_1

st.title("Fund addresses")
st.text(f"Admin address: {admin_address}")
st.text(f"Buyer 1 address: {buyer_1_address}")

nft_repository = NFTRepository()

if "nfts_deployed" not in st.session_state:
    st.session_state.nfts_deployed = False

if "should_deploy_apps" not in st.session_state:
    st.session_state.should_deploy_apps = True

if "NFT" not in st.session_state:
    st.session_state.NFT = NFTService(nft_creator_pk=admin_pk,
                                          nft_creator_address=admin_address,
                                          client=client,
                                          unit_name="bot",
                                          asset_name="NFT 76",
                                          nft_url="https://gateway.pinata.cloud/ipfs/QmZBiFNgb6hWj4JYwXc3PL5QqsoHYaGd4dNv2RWZZzSbjY")

# 1. Mint NFTS

def mint_NFT_nft():
    if st.session_state.NFT.nft_id is None:
        tx_id = st.session_state.NFT.create_nft()
        st.session_state.transactions.append(f"NFT 76 minted in {tx_id}")

st.title("Step 1: Mint NFTs")
buttons = st.columns(2)

if st.session_state.NFT.nft_id is None:
    _ = buttons[0].button("Mint NFT 76", on_click=mint_NFT_nft)
else:
    nft_id = st.session_state.NFT.nft_id
    if st.session_state.NFT_image is None:
        st.session_state.NFT_image = nft_repository.nft_image(nft_id)

    buttons[0].image(st.session_state.NFT_image,
                     caption=f"NFT 76 with nft_id: {nft_id}",
                     use_column_width=True)

    if "NFT_market" not in st.session_state:
        st.session_state.NFT_market = NFTMarketplace(admin_pk=admin_pk,
                                                         admin_address=admin_address,
                                                         nft_id=nft_id,
                                                         client=client)


time.sleep(2)

st.title("Step 2: Deploy Stateful Smart Contracts that enable the buy/sell interactions")

can_deploy = ("NFT_market" in st.session_state)
if can_deploy and st.session_state.should_deploy_apps:
    st.warning("Deploying of the Stateful Smart Contracts started...")

    tx_id = st.session_state.NFT_market.app_initialization(nft_owner_address=admin_address)
    st.session_state.transactions.append(f"ASC1 for NFT 76 deployed in {tx_id}")


    tx_id = st.session_state.NFT.change_nft_credentials_txn(
        escrow_address=st.session_state.NFT_market.escrow_address)
    st.session_state.transactions.append(f"NFT credentials changed for NFT 76 in {tx_id}")


    tx_id = st.session_state.NFT_market.initialize_escrow()
    st.session_state.transactions.append(f"Escrow for NFT 76 initialized in {tx_id}")


    tx_id = st.session_state.NFT_market.fund_escrow()
    st.session_state.transactions.append(f"Escrow for NFT 76 funded in {tx_id}")


    st.session_state.should_deploy_apps = False
    st.session_state.app_is_deployed = True
else:
    if not can_deploy:
        st.error("You firs need to mint the NFTs.")
    else:
        st.success("Stateful Smart Contracts were successfully deployed.")


def sell_NFT(sell_price: int):
    nft_owner_pk = st.session_state.NFT_owner[0]
    tx_id = st.session_state.NFT_market.make_sell_offer(sell_price=sell_price,
                                                            nft_owner_pk=nft_owner_pk)
    st.session_state.transactions.append(f"NFT 76 is put on sale for {sell_price} micro algos in {tx_id}")


def buy_NFT(buy_price: int, owner_address):
    tx_id = st.session_state.NFT.opt_in(buyer_1_pk)
    st.session_state.transactions.append(f"Account opted-in for NFT 76 in {tx_id}")

    tx_id = st.session_state.NFT_market.buy_nft(nft_owner_address=owner_address,
                                                    buyer_address=buyer_1_address,
                                                    buyer_pk=buyer_1_pk,
                                                    buy_price=buy_price)
    st.session_state.transactions.append(f"NFT 76 bought by {buyer_1_address} in {tx_id}")
    st.session_state.NFT_owner = st.session_state.buyer_1



if st.session_state.app_is_deployed:
    st.title("Step 3: Buy/Sell the NFTs")

    NFT_app_state = NFTMarketplaceRepository.load_app_state(st.session_state.NFT_market.app_id)

    st.image(st.session_state.NFT_image,
             caption=f"NFT 76 connected with asc1: {st.session_state.NFT_market.app_id}")

    if NFT_app_state["APP_STATE"] == 1:
        st.warning("The NFT 76 is not on SALE")
        price_NFT = st.number_input(f'NFT 76 Price',
                                        value=1000000,
                                        step=100)
        _ = st.button(f'Sale NFT 76 for {price_NFT} micro algos', on_click=sell_NFT,
                      args=(price_NFT,))
    else:
        nft_price = NFT_app_state["ASA_PRICE"]
        nft_seller = NFT_app_state["ASA_OWNER"]
        st.success(f"The NFT 76 is on sale for: {nft_price} micro algos by: {nft_seller}")
        _ = st.button(f'Buy NFT 76', on_click=buy_NFT,
                      args=(nft_price, nft_seller))


st.title("Executed transactions")

for tx in st.session_state.transactions:
    st.success(tx)
