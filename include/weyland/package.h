/******************************************************************************/
/*!
	Copyright (c) 2014 Surtr Studios. All Rights Reserved.

@file	package.h
@brief	Defines the interface for the Package class.
*/
/******************************************************************************/

/*** Include Guard ************************************************************/
#ifndef WEYLAND_PACKAGE_H_
#define WEYLAND_PACKAGE_H_

/*** Includes *****************************************************************/
#include <string>
#include <vector>

namespace weyland {

	/**************************************************************************/
	/*!
	 * @brief	Represents a Weyland build package.
	 */
	/**************************************************************************/
	class Package {
	public:
		// Constructor
		Package();
		Package(std::string name);
		Package(std::string name, std::string version);
		// Destructor
		virtual ~Package();

		// Mutators and accessors
		inline std::string name() const						{ return mName; }
		inline std::string version() const 					{ return mVersion; }
		inline std::vector<std::string> targets() const 	{ return mTargets; }

	private:
		std::string mName;
		std::string mVersion;
		std::vector<std::string> mTargets;
	};
}		/* namespace weyland */
#endif 	/* WEYLAND_PACKAGE_H_ */
