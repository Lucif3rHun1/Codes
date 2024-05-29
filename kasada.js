// exact same package they use for sha256, just not minified/"web-ified"
const sha256 = require('js-sha256')

let hashDifficulty = function (arg1) {
  return (
    0x10000000000000 / (Number('0x'['concat'](arg1['slice'](0x0, 0xd))) + 0x1)
  )
}

let __ = (inputs, timestamp, secret) => {
  var initialHash = sha256.sha256(
    `${inputs.platformInputs}, ${timestamp}, ${secret}`
  )
  var subchallengeDifficulty = inputs.difficulty / inputs.subchallengeCount
  var subchallengeResults = []

  for (var i = 0; i < inputs.subchallengeCount; i++) {
    var nonce = 1

    while (true) {
      var currentHash = sha256.sha256(`${nonce}, ${initialHash}`)

      if (hashDifficulty(currentHash) >= subchallengeDifficulty) {
        subchallengeResults.push(nonce)
        initialHash = currentHash
        break
      }

      nonce++
    }
  }

  return {
    answers: subchallengeResults,
    finalHash: initialHash
  }
}

let makeId = function () {
  let result = ''
  for (let i = 0; i < 32; i++) {
    result += '0123456789abcdef'[Math.floor(16 * Math.random())]
  }
  return result
}

let startTime = Date.now()
let response = __(
  {
    platformInputs: 'tp-v2-input',
    difficulty: 10,
    subchallengeCount: 2
  }, // challenge-config : not changed
  startTime, // challenge-st(starttime) : yes
  makeId() // random id to check for hashing
)

console.log(response)