

template_layerentry = """
	{index} = {{
		factor = 50
		modifier = {{
			factor = 0
			NOT = {{ trait = portrait_{name} }}
		}}
		{agemodifiers}
	}}
"""

template_layerentry_minage = """
		modifier = {{
			factor = 0
			practical_age < {age}	
		}}
"""
template_layerentry_maxage = """
		modifier = {{
			factor = 0
			practical_age > {age}	
		}}
"""

template_layerentry_blank = """
	# blank
	0 = {{
		factor = 100
		{noblank_modifiers}
	}}
"""

template_noblank = """
		modifier = {{
			factor = 0
			trait = portrait_{name}
		}}	
"""


template_sprite = """
	spriteType = {{
		name = "{reference}"
		texturefile = "{filename}"
		noOfFrames = {frames}
		norefcount = yes
		can_be_lowres = yes
	}}
"""

template_portraittype = """
	portraitType = {{
		name = "PORTRAIT_{spritename}"

		weight = {{
			additive_modifier = {{
				value = 1000000 #vanilla uses 10000
				portrait_clothing = yes
				OR = {{
					{conditions_portrait_trait}
				}}
			}}
		}}

		layer = {{
			"GFX_empty:c0"
			"GFX_empty:c2"
			"GFX_empty:c3"
			"GFX_empty:c1"
			"GFX_empty:c4"
			"GFX_empty:p1:h:y"
			"GFX_character_static_0:c5"
		}}

		allow_property_values = {{
			5 = {{
				0 = {{ always = no }}
				{portrait_props}
			}}
		}}
	}}

"""
template_condition_portraittrait = """
					portrait_has_trait = portrait_{name}
"""
template_portrait_prop = """
				{index} = {{ always = yes }}
"""

template_trait = """
portrait_{name} = {{
	customizer = no
	random = no
	hidden = yes	
	#cached = yes
}}
"""
