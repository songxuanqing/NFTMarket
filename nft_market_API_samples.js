// curl -d "dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&nft_owner_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&nft_owner_pk=/8qKTp3HAFjgGiStk2wjKBx2dZ2PDzxziDG6y0GIltiH1y7WmJvr9qmMUWetZ2DQ7SPSEAf4hZfuvFTG7PGH6g==&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080&unit_name=piece&asset_name=piece&nft_url=https://gateway.pinata.cloud/ipfs/QmZBiFNgb6hWj4JYwXc3PL5QqsoHYaGd4dNv2RWZZzSbjY" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/create_nft
//NFT생성하기
$.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/create_nft",
    crossDomain: true,
    contentType:'application/x-www-form-urlencoded',
    data: {
        dev_address:'FM2ITBJFYMINMCPRQLPGUUCLQOLEEZ2BHTE6CP2AEMKF7QTJOI5GIPM4KU',
        dev_pk:'IfyM4vCYgYa23Vk/wixySpQXcx4aqsij+Oa6ZWX40UErNImFJcMQ1gnxgt5qUEuDlkJnQTzJ4T9AIxRfwmlyOg==',
        nft_owner_address:'4Q7QX52TW7TJARQGYYWV2RDRGL7LEUK34WXQECKDCLBTCLGNBEDXAAJ2YY',
        nft_owner_pk:'01Lo297AbcmD8zv0Nh+LV0YadUdRE59fZxATtdUI/JPkPwv3U7fmkEYGxi1dRHEy/rJRW+WvAglDEsMxLM0JBw==',
        unit_name:'piece',
        asset_name:'piece',
        nft_url:'https://gateway.pinata.cloud/ipfs/QmZBiFNgb6hWj4JYwXc3PL5QqsoHYaGd4dNv2RWZZzSbjY.json',
        token:'212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d',
        ip_address:'http://127.0.0.1:43615'
    },
    success: function(response){
       console.log(response)
    }
  })

// {
//   "nft_id": 94433012,
//   "result": "success",
//   "txn_id": "HHNLPS45H3M7WMWO4LVS7Y55WVOQC4GBFSEEM4GI53FWNTPAGRCA"
// }



// curl -d "dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&nft_owner_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&nft_id=94445264&token_id=94434081&sell_price=100&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/sell_nft
//NFT판매하기
$.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/sell_nft",
    crossDomain: true,
    contentType:'application/x-www-form-urlencoded',
    data: {
        dev_address:'FM2ITBJFYMINMCPRQLPGUUCLQOLEEZ2BHTE6CP2AEMKF7QTJOI5GIPM4KU',
        dev_pk:'IfyM4vCYgYa23Vk/wixySpQXcx4aqsij+Oa6ZWX40UErNImFJcMQ1gnxgt5qUEuDlkJnQTzJ4T9AIxRfwmlyOg==',
        nft_owner_address:'4Q7QX52TW7TJARQGYYWV2RDRGL7LEUK34WXQECKDCLBTCLGNBEDXAAJ2YY',
        nft_id:321,
        token_id:147,
        sell_price:100,
        token:'212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d',
        ip_address:'http://127.0.0.1:43615'
    },
    success: function(response){
       console.log(response)
    }
  })
// {
//   "app_id": 94434187,
//   "result": "success",
//   "txn_id": "ST6PGO2LODF5LLXAT5LLDSEUGC57FA7HBRX6AZQ2H4TGUFCUZT6Q"
// }



// curl -d "nft_owner_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&nft_owner_pk=/8qKTp3HAFjgGiStk2wjKBx2dZ2PDzxziDG6y0GIltiH1y7WmJvr9qmMUWetZ2DQ7SPSEAf4hZfuvFTG7PGH6g==&dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&buyer_address=CSWVHEEZDZQR452LEYCJGNBRDZU7SSKANOA32OPOKNBMYJSAV5BNZEXIXA&buyer_pk=zgoVj7FaDmVMwmJ/A8LvZvTMylApD3cXEyphl8Vi/wQUrVOQmR5hHndLJgSTNDEeaflJQGuBvTnuU0LMJkCvQg==&nft_id=94445264&app_id=94445368&buy_price=100&token_id=94434081&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/buy_nft
//NFT구매하기
$.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/buy_nft",
    crossDomain: true,
    contentType:'application/x-www-form-urlencoded',
    data: {
        nft_owner_address:'4Q7QX52TW7TJARQGYYWV2RDRGL7LEUK34WXQECKDCLBTCLGNBEDXAAJ2YY',
        nft_owner_pk:'01Lo297AbcmD8zv0Nh+LV0YadUdRE59fZxATtdUI/JPkPwv3U7fmkEYGxi1dRHEy/rJRW+WvAglDEsMxLM0JBw==',
        dev_address:'FM2ITBJFYMINMCPRQLPGUUCLQOLEEZ2BHTE6CP2AEMKF7QTJOI5GIPM4KU',
        dev_pk:'IfyM4vCYgYa23Vk/wixySpQXcx4aqsij+Oa6ZWX40UErNImFJcMQ1gnxgt5qUEuDlkJnQTzJ4T9AIxRfwmlyOg==',
        buyer_address:'V6RTLD2D6I6N25LLSLMCRHFZDFSGBQPO3G6L57W6O3GZFGHSBSCBTKTTNU',
        buyer_pk:'Hq2N4DPpa8M+daaoOCrmdfSsbUNvmIAxDbpIxbxQyFqvozWPQ/I83XVrktgonLkZZGDB7tm8vv7eds2SmPIMhA==',
        nft_id:321,
        app_id:322,
        buy_price:100,
        token_id:147,
        token:'212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d',
        ip_address:'http://127.0.0.1:43615'
    },
    success: function(response){
       console.log(response)
    }
  })
// {
//   "result": "success",
//   "txn_id": "LBUJQK3TIQKWBGRBFS6V2EQ3LDMXDSV7BGZPEQ5274DRUA7LEPVQ"
// }


// curl -d "dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&nft_owner_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&nft_id=94440538&app_id=94440641&token_id=94434081&sell_price=100&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/stop_sell
//NFT판매 중지하기
$.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/stop_sell",
    crossDomain: true,
    contentType:'application/x-www-form-urlencoded',
    data: {
        dev_address:'FM2ITBJFYMINMCPRQLPGUUCLQOLEEZ2BHTE6CP2AEMKF7QTJOI5GIPM4KU',
        dev_pk:'IfyM4vCYgYa23Vk/wixySpQXcx4aqsij+Oa6ZWX40UErNImFJcMQ1gnxgt5qUEuDlkJnQTzJ4T9AIxRfwmlyOg==',
        nft_owner_address:'4Q7QX52TW7TJARQGYYWV2RDRGL7LEUK34WXQECKDCLBTCLGNBEDXAAJ2YY',
        nft_id:321,
        app_id:322,
        token_id:147,
        sell_price:100,
        token:'212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d',
        ip_address:'http://127.0.0.1:43615'
    },
    success: function(response){
       console.log(response)
    }
  })

// curl -d "receiver_pk=zgoVj7FaDmVMwmJ/A8LvZvTMylApD3cXEyphl8Vi/wQUrVOQmR5hHndLJgSTNDEeaflJQGuBvTnuU0LMJkCvQg==&token_id=94434081&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/token_optin
//Token Optin
$.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/token_optin",
    crossDomain: true,
    contentType:'application/x-www-form-urlencoded',
    data: {
        receiver_pk:'01Lo297AbcmD8zv0Nh+LV0YadUdRE59fZxATtdUI/JPkPwv3U7fmkEYGxi1dRHEy/rJRW+WvAglDEsMxLM0JBw==',
        token_id:147,
        token:'212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d',
        ip_address:'http://127.0.0.1:43615'
    },
    success: function(response){
       console.log(response)
    }
  })
// {
//   "result": "success",
//   "txn_id": "IXMUS4BXIDDPEWXLGOYAWT5CVMLI5JBCNV3WIMJTIFP4VZIZMFYQ"
// }

// curl -d "dev_address=5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU&dev_pk=BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==&sender_address=CSWVHEEZDZQR452LEYCJGNBRDZU7SSKANOA32OPOKNBMYJSAV5BNZEXIXA&receiver_address=Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU&token_id=94434081&amount=1000&token=158a0082b552fe50d446f53329c972985de0c4ae43d5b2fd1bebc443b077cf59&ip_address=http://127.0.0.1:8080" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/token_transfer
//token transfer, 개발사가 sender의 토큰 보유 권한을 박탈하고, receiver에게 토큰을 전송한다.
$.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/token_transfer",
    crossDomain: true,
    contentType:'application/x-www-form-urlencoded',
    data: {
        dev_address:'5QX5D4HPXQIQ3ODMGN6NTH6GO435N5GJSA72FBKSJI4WCAJ5VAXWTAF6UU',
        dev_pk:'BFChzShBzM561pMUeZ3I7hTEurXr+ZoMzn27aQ8sV3jsL9Hw77wRDbhsM3zZn8Z3N9b0yZA/ooVSSjlhAT2oLw==',
        sender_address:'CSWVHEEZDZQR452LEYCJGNBRDZU7SSKANOA32OPOKNBMYJSAV5BNZEXIXA',
        receiver_address:'Q7LS5VUYTPV7NKMMKFT22Z3A2DWSHUQQA74ILF7OXRKMN3HRQ7VC57EELU',
        token_id:147,
        amount:1000,
        token:'212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d',
        ip_address:'http://127.0.0.1:43615'
    },
    success: function(response){
       console.log(response)
    }
  })


// curl -d "sender_address=FD3NQJQ4S6NDIGNTJ2C2LSCKZHC2PDPGSURBIUPTQWYBK64V7FQPUSUNXU&sender_pk=01Lo297AbcmD8zv0Nh%2BLV0YadUdRE59fZxATtdUI/JPkPwv3U7fmkEYGxi1dRHEy/rJRW%2BWvAglDEsMxLM0JBw==&receiver_address=6LB7WPUK3ZBX73F4YEM5TBUCHLLRCVBB5KGZQZE6CKKNVPR7A6S5RRD3FE&amount=100&token=212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d&ip_address=http://127.0.0.1:33755" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://127.0.0.1:5000/nova_payment
//nova payment
$.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/nova_payment",
    crossDomain: true,
    contentType:'application/x-www-form-urlencoded',
    data: {
        sender_address:'FD3NQJQ4S6NDIGNTJ2C2LSCKZHC2PDPGSURBIUPTQWYBK64V7FQPUSUNXU',
        sender_pk:'01Lo297AbcmD8zv0Nh+LV0YadUdRE59fZxATtdUI/JPkPwv3U7fmkEYGxi1dRHEy/rJRW+WvAglDEsMxLM0JBw==',
        receiver_address:'6LB7WPUK3ZBX73F4YEM5TBUCHLLRCVBB5KGZQZE6CKKNVPR7A6S5RRD3FE',
        amount:100,
        token:'212ba0a5ae0335a1443d52dd0af48b51305f621d02a58a267a9dd4985347b90d',
        ip_address:'http://127.0.0.1:43615'
    },
    success: function(response){
       console.log(response)
    }
  })
