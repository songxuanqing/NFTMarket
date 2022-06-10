from src.blockchain_utils.credentials import get_client, get_account_credentials
from src.services.nft_service import NFTService
from src.services.nft_marketplace import NFTMarketplace

client = get_client()
admin_pk, admin_addr, _ = get_account_credentials(1)
buyer_pk, buyer_addr, _ = get_account_credentials(2)

nft_service = NFTService(nft_creator_address=admin_addr,
                         nft_creator_pk=admin_pk,
                         client=client,
                         asset_name="piece",
                         unit_name="piece")
print("NFT서비스 객체 생성 완료")
nft_service.create_nft()
print("NFT생성 완료")
nft_marketplace_service = NFTMarketplace(admin_pk=admin_pk,
                                         admin_address=admin_addr,
                                         client=client,
                                         nft_id=nft_service.nft_id)
print("NFT마켓플레이스 서비스 생성 완료")
nft_marketplace_service.app_initialization(nft_owner_address=admin_addr)
print("NFT마켓 앱 초기화 완료")
nft_service.change_nft_credentials_txn(escrow_address=nft_marketplace_service.escrow_address)
print("NFT크리덴션 트랜잭션 완료")
nft_marketplace_service.initialize_escrow()
print("NFT마켓플레이스 에스크로(임치) 완료")
nft_marketplace_service.fund_escrow()
print("NFT마켓플레이스 펀드 임치 완료")
nft_marketplace_service.make_sell_offer(sell_price=100000, nft_owner_pk=admin_pk)
print("NFT판매등록 완료")
nft_service.opt_in(buyer_pk)
print("NFT판매자 옵트인 완료")
nft_marketplace_service.buy_nft(nft_owner_address=admin_addr,
                                buyer_address=buyer_addr,
                                buyer_pk=buyer_pk,
                                buy_price=100000)
print("NFT구매하기 완료")