import codecs
import math

import pytest

import shamir_mnemonic

from .api		import create, group_parser
from .recovery		import recover
from .defaults		import GROUPS, GROUP_THRESHOLD_RATIO

from .dependency_test	import substitute, nonrandom_bytes

SEED_FF_HEX			= 'ff' * 16
SEED_FF				= codecs.decode( SEED_FF_HEX, 'hex_codec' )


@substitute( shamir_mnemonic.shamir, 'RANDOM_BYTES', nonrandom_bytes )
def test_passphrase():
    """Confirm that the default ff x 16 seed w/ no passphrase results in the expected default SLIP39
    Mnemonics, and the expected ETH 0x824b... and BTC bc1q9y... wallets.  These are confirmed as
    being consistent w/ the Trezor.

    Also confirm that we implement SLIP39 passphrases correctly, compared to the Satoshi Labs:

        $ shamir recover -p
        Enter a recovery share: academic acid acrobat romp dining employer endless speak main stick database tenant alarm wealthy plan amuse credit crush arcade cylinder

        Completed 1 of 2 groups needed:
        ✓ 1 of 1 shares needed from group academic acid acrobat
        ✗ 0 shares from group academic acid beard
        ✗ 0 shares from group academic acid ceramic
        ✗ 0 shares from group academic acid decision
        Enter a recovery share: academic acid beard romp dismiss mayor juice glance twice response eclipse inmate muscle climate born increase reject typical slow evil

        Completed 2 of 2 groups needed:
        ✓ 1 of 1 shares needed from group academic acid acrobat
        ✓ 1 of 1 shares needed from group academic acid beard
        ✗ 0 shares from group academic acid ceramic
        ✗ 0 shares from group academic acid decision
        Enter passphrase: password
        Repeat for confirmation: password
        SUCCESS!
        Your master secret is: ffffffffffffffffffffffffffffffff

    """
    groups			= dict(
        group_parser( g )
        for g in GROUPS
    )
    group_threshold		= math.ceil( len( groups ) * GROUP_THRESHOLD_RATIO )

    details_nonpass		= create(
        name		= "SLIP39 Wallet: FF",
        group_threshold	= group_threshold,
        groups		= groups,
        master_secret	= SEED_FF,
        extendable	= False,
    )
    #print( json.dumps( details_nonpass.groups, indent=4 ))
    assert details_nonpass.groups == {
        "First": (
            1,
            [
                "academic acid acrobat romp change injury painting safari drug browser trash fridge busy finger standard angry similar overall prune ladybug"
            ]
        ),
        "Second": (
            1,
            [
                "academic acid beard romp believe impulse species holiday demand building earth warn lunar olympic clothes piece campus alpha short endless"
            ]
        ),
        "Fam": (
            2,
            [
                "academic acid ceramic roster desire unwrap depend silent mountain agency fused primary clinic alpha database liberty silver advance replace medical",
                "academic acid ceramic scared column screw hawk dining invasion bumpy identify anxiety august sunlight intimate satoshi hobo traveler carbon class",
                "academic acid ceramic shadow believe revenue type class station domestic already fact desktop penalty omit actress rumor beaver forecast group",
                "academic acid ceramic sister actress mortgage random talent device clogs craft volume cargo item scramble easy grumpy wildlife wrist simple"
            ]
        ),
        "Frens": (
            3,
            [
                "academic acid decision round academic academic academic academic academic academic academic academic academic academic academic academic academic ranked flame amount",
                "academic acid decision scatter biology trial escape element unfair cage wavy afraid provide blind pitch ultimate hybrid gravity formal voting",
                "academic acid decision shaft crunch glance exclude stilt grill numb smug stick obtain raisin force theater duke taught license scramble",
                "academic acid decision skin disaster mama alive nylon mansion listen cowboy suitable crisis pancake velvet aviation exhaust decent medal dominant",
                "academic acid decision snake aunt frozen flip crystal crystal observe equip maximum maiden dragon wine crazy nervous crystal profile fiction",
                "academic acid decision spider bulge receiver behavior humidity ruler luck public math distance cylinder fantasy seafood training withdraw payment playoff"
            ]
        )
    }

    [(eth,btc)] 		= details_nonpass.accounts
    assert eth.path == "m/44'/60'/0'/0/0"
    assert eth.address == '0x824b174803e688dE39aF5B3D7Cd39bE6515A19a1'
    assert btc.path == "m/84'/0'/0'/0/0"
    assert btc.address == 'bc1q9yscq3l2yfxlvnlk3cszpqefparrv7tk24u6pl'

    # Ensure we can recover it w/ no passphrase
    assert recover(
        details_nonpass.groups['Fam'][1][:2] + details_nonpass.groups['Frens'][1][:-3],
    ) == SEED_FF

    # Now, ensure that we see a different set of Mnemonics w/ a SLIP39 passphrase.

    # NOTE: this is NOT what the Trezor uses when you enter a "hidden" wallet passphrase!  There is
    # no support for SLIP39 passphrase decryption on the Trezor.  However, confirm that it works as
    # specified by the shamir_mnemonic module.

    # First, ensure we do *not* recover the origin seed when we use an incorrect passphrase with the
    # Mnemonics generated with *not* passphrase.

    badpass			= "password".encode( 'UTF-8' )

    assert recover(
        details_nonpass.groups['Fam'][1][:2] + details_nonpass.groups['Frens'][1][:-3],
        passphrase	= badpass,
    ) != SEED_FF

    details_badpass		= create(
        name		= "SLIP39 Wallet: FF",
        group_threshold	= group_threshold,
        groups		= groups,
        master_secret	= SEED_FF,
        passphrase	= badpass,
        extendable	= False,
    )
    #print( json.dumps( details_badpass.groups, indent=4 ))
    assert details_badpass.groups == {
        "First": (
            1,
            [
                "academic acid acrobat romp dining employer endless speak main stick database tenant alarm wealthy plan amuse credit crush arcade cylinder"
            ]
        ),
        "Second": (
            1,
            [
                "academic acid beard romp dismiss mayor juice glance twice response eclipse inmate muscle climate born increase reject typical slow evil"
            ]
        ),
        "Fam": (
            2,
            [
                "academic acid ceramic roster answer charity ceiling mason kernel jerky woman laundry duckling dining dress grumpy lily fortune cleanup black",
                "academic acid ceramic scared dwarf quarter adequate umbrella inform hamster grief album broken humidity lecture domain estimate losing revenue mouse",
                "academic acid ceramic shadow cluster cards artwork wrap grief forbid skin ordinary vocal lunar engage sister sugar pink maximum cover",
                "academic acid ceramic sister benefit marathon database ordinary hawk equation fawn thorn soldier taste welcome mild blimp insect born pistol"
            ]
        ),
        "Frens": (
            3,
            [
                "academic acid decision round academic academic academic academic academic academic academic academic academic academic academic academic academic ranked flame amount",
                "academic acid decision scatter become flavor crystal genuine hour infant voice unfair recall living afraid company froth distance bundle soldier",
                "academic acid decision shaft display headset level prevent verdict genius preach glad makeup element twin scene hunting smoking rival mortgage",
                "academic acid decision skin course dress prisoner skunk ordinary blind freshman member drink scroll traffic thank deliver frequent velvet evoke",
                "academic acid decision snake burden unknown guard peaceful artwork snapshot teaspoon literary move spray saver voice august maximum hazard negative",
                "academic acid decision spider ancestor regular evaluate salon glasses penalty blue guitar check extra roster snapshot fantasy adjust coastal eclipse"
            ]
        )
    }

    # Now, without the correct password, we can't recover the original SEED_FF.  We *do* recover "a"
    # seed: there is no verification/validation that the supplied passphrase was "correct".  You
    # simply are expected to know that the derived wallet(s) are the ones you expect.  This is by
    # design -- you can supply an attacker with a "duress" seed passphrase leading to wallet(s) with
    # a small sacrificial amount of funds.
    assert recover(
        details_badpass.groups['Fam'][1][:2] + details_badpass.groups['Frens'][1][:3],
    ) != SEED_FF
    assert recover(
        details_badpass.groups['Fam'][1][:2] + details_badpass.groups['Frens'][1][:3],
        passphrase	= badpass,
    ) == SEED_FF

    # Mixing SLIP39 recovery groups should fail to recover, both without and with the password,
    # since SLIP39 confirms the digest of the recovered "encrypted" seed, before decryption.  This
    # was the default, before SLIP-39 added the concept of "extendable".
    with pytest.raises( shamir_mnemonic.utils.MnemonicError ):
        assert recover(
            details_nonpass.groups['Fam'][1][:2] + details_badpass.groups['Frens'][1][:3],
        ) != SEED_FF
    with pytest.raises( shamir_mnemonic.utils.MnemonicError ):
        assert recover(
            details_nonpass.groups['Fam'][1][:2] + details_badpass.groups['Frens'][1][:3],
            passphrase	= badpass,
        ) != SEED_FF

    # And finally, confirm that the SLIP39 Mnemonics protected by the correct passphrase also yield
    # the expected ETH and BTC wallets.  This is obviously the expected behaviour, because the
    # SLIP39 passphrase simply encrypts/decrypts the original seed.
    [(eth,btc)] 		= details_badpass.accounts
    assert eth.path == "m/44'/60'/0'/0/0"
    assert eth.address == '0x824b174803e688dE39aF5B3D7Cd39bE6515A19a1'
    assert btc.path == "m/84'/0'/0'/0/0"
    assert btc.address == 'bc1q9yscq3l2yfxlvnlk3cszpqefparrv7tk24u6pl'
