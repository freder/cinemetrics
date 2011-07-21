# -*- coding: utf-8 -*-
import sys
import os
import glob


def main():
	os.chdir(sys.argv[1])
	
	file_string = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
	<?aid style="50" type="snippet" readerVersion="6.0" featureSet="257" product="6.0(622)" ?>
	<?aid SnippetType="PageItem"?>
	<Document DOMVersion="6.0" Self="d">
		<Spread Self="spread">
			<TextFrame Self="textframe" ParentStory="story" ContentType="TextType">
				<Properties>
					<PathGeometry>
						<GeometryPathType PathOpen="false">
							<PathPointArray>
								<PathPointType Anchor="-269.29133858258666 -392.5984251960866" LeftDirection="-269.29133858258666 -392.5984251960866" RightDirection="-269.29133858258666 -392.5984251960866"/>
								<PathPointType Anchor="-269.29133858258666 392.5984251960866" LeftDirection="-269.29133858258666 392.5984251960866" RightDirection="-269.29133858258666 392.5984251960866"/>
								<PathPointType Anchor="269.29133858258666 392.5984251960866" LeftDirection="269.29133858258666 392.5984251960866" RightDirection="269.29133858258666 392.5984251960866"/>
								<PathPointType Anchor="269.29133858258666 -392.5984251960866" LeftDirection="269.29133858258666 -392.5984251960866" RightDirection="269.29133858258666 -392.5984251960866"/>
							</PathPointArray>
						</GeometryPathType>
					</PathGeometry>
				</Properties>
			</TextFrame>
		</Spread>
		<Story Self="story">
	'''
	
	os.chdir("shot_slitscans")
	for i, file in enumerate( glob.glob("*.png") ):
		file_path = os.path.abspath(file).replace("\\", "/")
		#print file_path
		file_string += '''
		<Rectangle Self="rect_%d" ContentType="GraphicType">
			<Image Self="img_%d" ItemTransform="0.2 0 0 0.2 0 0">
				<Properties>
					<GraphicBounds Left="0" Top="0" Right="200" Bottom="200"/>
				</Properties>
				<Link Self="link_%d" LinkResourceURI="file:%s" />
			</Image>
		</Rectangle>
	''' % (i, i, i, file_path)

	file_string += '''
		</Story>
	</Document>
	'''

	f = open(r"..\shot_slitscans.idms", "w")
	f.write(file_string)
	f.close()


# #########################
if __name__ == "__main__":
	main()
# #########################
