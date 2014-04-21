/******************************************************************************/
/*!
	Copyright (c) 2014 Surtr Studios. All Rights Reserved.

@file	package.cc
@brief	Implements the package class.
*/
/******************************************************************************/

/*** Includes *****************************************************************/
#include "weyland/package.h"

/******************************************************************************/
/*!
 * @brief	Initializes a new instance of the Package class using default
 * 			values.
 */
/******************************************************************************/
weyland::Package::Package()
	: mName("")
	, mVersion("dev") 
	, mTargets() {
}

/******************************************************************************/
/*!
 * @brief	Initializes a new instance of the Package class using the given
 * 			name.
 * @param	name	The name of the Package instance to create.
 */
/******************************************************************************/
weyland::Package::Package(std::string name)
	: mName(name)
	, mVersion("dev")
	, mTargets()  {
}

/******************************************************************************/
/*!
 * @brief	Initializes a new instance of the Package class using the given
 * 			values.
 * @param	name	The name of the Package instance to create.
 * @param	version	The version of the Package instance to create.
 */
/******************************************************************************/
weyland::Package::Package(std::string name, std::string version)
	: mName(name)
	, mVersion(version)
	, mTargets()  {
}

/******************************************************************************/
/*!
 * @brief	Destroys an instance of the Package class and performs any
 * 			necessary clean-up actions.
 */
/******************************************************************************/
weyland::Package::~Package() {
}
