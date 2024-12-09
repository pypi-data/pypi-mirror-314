import qrcode

from pytest 		import approx
from fpdf		import FPDF, FlexTemplate

from .layout		import Region, Text, Image, Box, Coordinate
from .defaults		import MM_IN


def test_Region():
    card_size			= Coordinate( y=2+1/4, x=3+3/8 )
    card_margin    		= 1/8
    card			= Box( 'card', 0, 0, card_size.x, card_size.y )
    #print( card )
    card_interior		= card.add_region_relative(
        Region( 'card-interior', x1=+card_margin, y1=+card_margin, x2=-card_margin, y2=-card_margin )
    )
    #print( card_interior )
    assert card_interior.x1 == card_margin
    assert card_interior.x2 == card_size.x - card_margin
    assert card_interior.y2 == card_size.y - card_margin
    assert card_interior.x2 - card_interior.x1 == card_size.x - card_margin * 2

    card_qr			= card_interior.add_region_proportional(
        Image( 'card-qr', x1=1/2, y1=1/4, x2=1, y2=1 )
    ).square( maximum=1, justify='BR' )
    card_interior.add_region_proportional(
        Box( 'card-box-ul', x1=1/2, y1=1/4, x2=1, y2=1 )
    ).square( maximum=.5, justify='TL' )
    card_interior.add_region_proportional(
        Box( 'card-box-cm', x1=1/2, y1=1/4, x2=1, y2=1 )
    ).square( maximum=.5 )
    card_interior.add_region_proportional(
        Box( 'card-box-br', x1=1/2, y1=1/4, x2=1, y2=1 )
    ).square( maximum=.5, justify='BR' )

    #card_qr.x1			= card_qr.x2 - 1.0
    #card_qr.y1			= card_qr.y2 - 1.0
    #print( card_qr )
    assert card_qr.x1 == 2.25
    assert card_qr.y1 == 1.125

    elements			= list( card.elements() )[1:]
    #print( json.dumps( elements, indent=4 ))
    assert len( elements ) == 4
    assert elements[0]['type'] == 'I'

    card_top			= card_interior.add_region_proportional(
        Region( 'card-top', x1=0, y1=0, x2=1, y2=1/3 )
    )
    card_top.add_region_proportional(
        Text( 'card-title', x1=0, y1=0, x2=1, y2=40/100 )
    )

    elements			= list( card.elements() )[1:]
    #print( json.dumps( elements, indent=4 ))
    assert elements[-1]['type'] == 'T'
    assert elements[-1]['font'] == 'helvetica'
    assert elements[-1]['size'] == approx( 14.4 )

    pdf				= FPDF()
    pdf.add_page()

    tpl				= FlexTemplate( pdf, list( card.elements() ) )
    tpl['card-qr']		= qrcode.make( 'abc' ).get_image()
    tpl['card-title']		= 'Abc'
    # Abc in upper-left
    tpl.render()

    tpl['card-qr']		= qrcode.make( 'abc' ).get_image()
    tpl['card-title']		= 'Xyz'
    # Xyz in lower-right
    tpl.render( offsetx = card_size.x * MM_IN, offsety = card_size.y * MM_IN )

    #pdf.output( "test.pdf" ) # To view results in test.pdf, uncomment
